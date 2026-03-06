import json
import google.generativeai as genai
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .itinerary_service import generate_smart_itinerary
from .models import TripPlan
from django.shortcuts import get_object_or_404

genai.configure(api_key=settings.AI_API_KEY)

@login_required
def trip_planner_view(request):
    if request.method == 'POST':
        # 1. Capture user inputs
        days = int(request.POST.get('days', 3))
        category = request.POST.get('category', 'ECO')
        state = request.POST.get('state', 'India')
        city = request.POST.get('city', '')

        # 2. Generate the itinerary via Gemini
        itinerary = generate_smart_itinerary(days, category, state, city)
        
        # Ensure itinerary is a list even if generation fails or returns something else
        if not isinstance(itinerary, list):
            itinerary = []

        if itinerary:
            # 3. SAVE to Database automatically
            # This allows the user to find it in "Saved Journeys" later
            TripPlan.objects.create(
                user=request.user,
                title=f"Expedition to {city or state}",
                days=days,
                interests=category,
                itinerary_data=itinerary
            )
        
        return render(request, 'ai_engine/itinerary_result.html', {
            'itinerary': itinerary,
            'days': days,
            'category': category,
            'state': state,
            'city': city
        })
    
    return render(request, 'ai_engine/planner_form.html')

@login_required
def trip_history_view(request):
    """Retrieve and display all saved trips for the logged-in user."""
    plans = TripPlan.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'ai_engine/trip_history.html', {'plans': plans})


@csrf_exempt
@login_required
def chatbot_query(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_msg = data.get('msg', '')
            
            # Using the validated 2.5 Lite model
            model = genai.GenerativeModel("gemini-2.5-flash-lite")
            
            # ENFORCE STRICT JSON OUTPUT
            instruction = (
                "You are a smart travel assistant. respond ONLY in valid JSON format. "
                "JSON Schema: "
                "{"
                "  \"city\": \"City Name\","
                "  \"safety_tips\": [\"tip1\", \"tip2\", \"tip3\"],"
                "  \"transport_tips\": [\"tip1\", \"tip2\", \"tip3\"],"
                "  \"cultural_tips\": [\"tip1\", \"tip2\", \"tip3\"],"
                "  \"top_places\": [{\"name\": \"Place Name\", \"description\": \"short description\"}]"
                "}"
            )
            
            # Use generation_config to force JSON if the SDK version supports it
            response = model.generate_content(
                f"{instruction} User Query: {user_msg}",
                generation_config={"response_mime_type": "application/json"}
            )
            
            # Parse the JSON response
            try:
                ai_data = json.loads(response.text)
                return JsonResponse({'reply': ai_data})
            except json.JSONDecodeError:
                # Fallback in case Gemini sends bad JSON
                return JsonResponse({'reply': {
                    "city": "Unknown",
                    "error": "Failed to generate structured data",
                    "raw": response.text
                }})

        except Exception as e:
            return JsonResponse({'reply': "My intelligence circuits are resetting. Please try again shortly!"})
            
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def chatbot_view(request):
    return render(request, 'ai_engine/chatbot.html')

@login_required
def trip_detail_view(request, plan_id):
    """View to display a previously saved trip plan."""
    # Retrieve the specific plan or return a 404 error
    plan = get_object_or_404(TripPlan, id=plan_id, user=request.user)
    
    # We reuse 'itinerary_result.html' to show the saved data
    return render(request, 'ai_engine/itinerary_result.html', {
        'itinerary': plan.itinerary_data,
        'days': plan.days,
        'category': plan.interests,
        'state': plan.title, # Title usually contains the state/city
        'is_saved_view': True # Flag to hide 'Save' logic if necessary
    })