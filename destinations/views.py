import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Avg, Count, Q

import base64
from django.http import JsonResponse
from django.conf import settings
from google import genai
from google.genai import types
from .models import Destination, ChatConversation, Itinerary

# Initialize GenAI Client
client = genai.Client(api_key=settings.AI_API_KEY)

# ----------------- AI CHATBOT (Monk-Style) -----------------

# Local App Imports
from .models import Destination, LocalGuide, Homestay
from .forms import DestinationForm, GuideAssignmentForm

User = get_user_model()

# Import AI Smart Ranking Logic
try:
    from ai_engine.logic import calculate_recommendation_score
except ImportError:
    def calculate_recommendation_score(avg_rating, sentiment_score, review_count):
        return 0

# --- TOURIST EXPLORATION VIEWS ---

def explore_view(request):
    category = request.GET.get('category')
    search_query = request.GET.get('search')
    
    # Base Query
    places_query = Destination.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        avg_sentiment=Avg('reviews__sentiment_score'),
        review_count=Count('reviews')
    )
    
    # Search logic: Checks name or description
    if search_query:
        places_query = places_query.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )
    
    if category:
        places_query = places_query.filter(category=category)

    # Convert to list for AI Scoring
    places_list = list(places_query)
    for place in places_list:
        place.smart_score = calculate_recommendation_score(
            place.avg_rating or 0, 
            place.avg_sentiment or 0, 
            place.review_count or 0
        )

    # Sort by AI Score
    sorted_places = sorted(places_list, key=lambda x: x.smart_score, reverse=True)

    return render(request, 'destinations/explore.html', {
        'places': sorted_places,
        'category': category,
        'search_query': search_query
    })

def place_detail_view(request, pk):
    place = get_object_or_404(Destination, pk=pk)
    guides = place.guides.filter(is_verified=True)
    homestays = place.homestays.all()
    reviews = place.reviews.all().order_by('-created_at')[:5]
    verified_guides = place.guides.filter(is_verified=True)
    verified_homestays = place.homestays.filter(is_verified=True)

    return render(request, 'destinations/place_detail.html', {
        'place': place,
        'guides': guides,
        'homestays': homestays,
        'reviews': reviews,
        'verified_guides': verified_guides,
        'verified_homestays': verified_homestays
    })

def interactive_map_view(request):
    places = Destination.objects.all()
    places_data = []
    for p in places:
        places_data.append({
            'name': p.name,
            'lat': p.latitude,
            'lng': p.longitude,
            'url': f"/destinations/place/{p.id}/",
            'category': p.get_category_display()
        })
    return render(request, 'destinations/map_view.html', {
        'places_json': json.dumps(places_data)
    })

# --- ADMIN GOVERNANCE VIEWS ---

@login_required
def add_destination(request):
    if request.user.role != 'admin':
        messages.warning(request, "Access Denied. Admin authority required.")
        return redirect('user_dashboard')

    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            new_place = form.save()
            messages.success(request, f"Registered {new_place.name} successfully.")
            return redirect('admin_dashboard')
    else:
        form = DestinationForm()
    return render(request, 'destinations/admin_add_place.html', {'form': form})

@login_required
def manage_services(request):
    """Authority View: Oversee the national network of Guides and Homestays."""
    if request.user.role != 'admin':
        return redirect('user_dashboard')
    
    # Handle Form Submission
    if request.method == 'POST':
        service_type = request.POST.get('service_type')
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        dest_id = request.POST.get('destination')
        destination = get_object_or_404(Destination, id=dest_id)

        # Logic to save to the correct model
        if service_type == 'guide':
            LocalGuide.objects.create(
                name=name, 
                phone=contact, # Field name in your LocalGuide model
                phone_number=contact,
                destination=destination, 
                is_verified=True
            )
        elif service_type == 'homestay':
            Homestay.objects.create(
                name=name, 
                contact=contact, # Field name in your Homestay model
                phone_number=contact,
                destination=destination, 
                is_verified=True
            )
        
        messages.success(request, f"New {service_type} attached to {destination.name} successfully!")
        return redirect('manage_services')

    # Fetch data for display
    context = {
        'guides': LocalGuide.objects.all().select_related('destination'),
        'homestays': Homestay.objects.all().select_related('destination'),
        'destinations': Destination.objects.all().order_by('name'),
    }
    return render(request, 'destinations/manage_services.html', context)

# --- USER MANAGER VIEWS (Fixed missing attributes) ---

@login_required
def user_manager_view(request):
    """Admin-only: Audit and manage registered users."""
    if request.user.role != 'admin':
        messages.error(request, "Unauthorized access.")
        return redirect('user_dashboard')
    
    users = User.objects.exclude(id=request.user.id).order_by('-date_joined')
    return render(request, 'accounts/user_manager.html', {'users': users})

@login_required
def toggle_user_status(request, user_id):
    """Admin-only: Activate or Deactivate a user account."""
    if request.user.role != 'admin':
        return redirect('user_dashboard')
    
    target_user = get_object_or_404(User, id=user_id)
    target_user.is_active = not target_user.is_active
    target_user.save()
    
    status = "activated" if target_user.is_active else "deactivated"
    messages.success(request, f"User {target_user.email} has been {status}.")
    return redirect('user_manager')

def chatbot_query(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_msg = data.get('msg', '')
            image_data = data.get('image', None)

            contents = []
            if user_msg: contents.append(user_msg)
            if image_data and "base64," in image_data:
                img_bytes = base64.b64decode(image_data.split("base64,")[1])
                contents.append(types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"))

            system_prompt = (
                "Role: Bharat AI - Jharkhand Tourism Guide. "
                "Tone: Helpful, respectful, and culturally rich. "
                "Task: Provide All Over India travel advice. Identify landmarks in images. "
                "CRITICAL: List mentioned places at the end under 'PLACES_FOUND:' "
                "followed by a comma-separated list of their exact database names."
            )

            response = client.models.generate_content(
                model="gemini-2.5-flash-lite", # Use the latest flash model
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.7,
                ),
            )

            bot_reply = response.text
            suggested_places = []
            
            if "PLACES_FOUND:" in bot_reply:
                main_text, place_part = bot_reply.split("PLACES_FOUND:")
                bot_reply = main_text.strip()
                names = [n.strip() for n in place_part.split(',') if n.strip()]
                places_qs = Destination.objects.filter(name__in=names)
                for p in places_qs:
                    suggested_places.append({'id': p.id, 'name': p.name, 'image': p.image.url})

            ChatConversation.objects.create(
                user=request.user if request.user.is_authenticated else None,
                message=user_msg or "[Sent Image]",
                response=bot_reply,
                is_anonymous=not request.user.is_authenticated
            )

            return JsonResponse({'reply': bot_reply, 'places': suggested_places})
        except Exception as e:
            return JsonResponse({'reply': "Connection interrupted. Try again.", 'error': str(e)}, status=500)

# ----------------- AI TRIP PLANNER -----------------
def itinerary_generator(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            days = int(data.get('days', 3))
            interests = data.get('interests', 'General')

            prompt = (
                f"Generate a {days}-day Jharkhand travel itinerary for: {interests}. "
                "Output ONLY a raw JSON array. Keys: 'day', 'time', 'activity', 'location'. "
                "No markdown, no backticks."
            )

            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )

            plan = json.loads(response.text)
            
            if request.user.is_authenticated:
                Itinerary.objects.create(
                    user=request.user, days=days, interests=interests, plan_data=plan
                )

            return JsonResponse({'plan': plan})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)