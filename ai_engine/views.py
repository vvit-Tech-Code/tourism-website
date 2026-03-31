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
        
        if itinerary:
            # 3. SAVE to Database automatically
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
    plans = TripPlan.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'ai_engine/trip_history.html', {'plans': plans})


# ================== 🔥 UPDATED CHATBOT ==================
@csrf_exempt
@login_required
def chatbot_query(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_msg = data.get('msg', '')

            model = genai.GenerativeModel("gemini-2.5-flash-lite")

            # 🔥 NEW STRICT JSON PROMPT
            instruction = """
You are Bharat AI, an expert Indian travel guide.

STRICT RULES:
- Return ONLY valid JSON
- No markdown, no explanations, no greetings

FORMAT:
{
  "state": "<state_name>",
  "safety": ["point1", "point2", "point3"],
  "transport": ["point1", "point2", "point3"],
  "culture": ["point1", "point2", "point3"],
  "hidden_gem": {
    "name": "<place_name>",
    "description": "<short description>"
  }
}

CONTENT RULES:
- Max 5 points per section
- Each point must be short and practical
"""

            response = model.generate_content(
                f"{instruction}\nUser: {user_msg}"
            )

            raw_text = response.text.strip()

            # 🔧 CLEAN MARKDOWN (Gemini sometimes adds ```json)
            if raw_text.startswith("```"):
                raw_text = raw_text.replace("```json", "").replace("```", "").strip()

            # 🔧 PARSE JSON SAFELY
            try:
                parsed = json.loads(raw_text)
            except Exception:
                parsed = {
                    "state": user_msg,
                    "safety": ["Unable to fetch structured data"],
                    "transport": [],
                    "culture": [],
                    "hidden_gem": {
                        "name": "",
                        "description": ""
                    }
                }

            return JsonResponse({
                'reply': parsed,
                'type': 'structured'
            })

        except Exception:
            return JsonResponse({
                'reply': "My intelligence circuits are resetting. Try again in a minute!",
                'type': 'error'
            })

    return JsonResponse({'error': 'Invalid request'}, status=400)
# ======================================================


@login_required
def chatbot_view(request):
    return render(request, 'ai_engine/chatbot.html')


@login_required
def trip_detail_view(request, plan_id):
    plan = get_object_or_404(TripPlan, id=plan_id, user=request.user)
    
    return render(request, 'ai_engine/itinerary_result.html', {
        'itinerary': plan.itinerary_data,
        'days': plan.days,
        'category': plan.interests,
        'state': plan.title,
        'is_saved_view': True
    })