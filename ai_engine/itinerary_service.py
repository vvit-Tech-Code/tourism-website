import json
import google.generativeai as genai
from django.conf import settings

def generate_smart_itinerary(days, category, state, city=""):
    """
    Requirement: AI National Trip Planner.
    Generates a day-wise itinerary for any state in India using Gemini.
    """
    genai.configure(api_key=settings.AI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    
    location = f"{city}, {state}" if city else state
    
    # System prompt forces Gemini to act as a structured data provider
    prompt = f"""
    Act as a professional Indian travel consultant. 
    Generate a {days}-day itinerary for {location}, India.
    Theme: {category} (Eco-Tourism or Cultural Heritage focus).
    
    Output format must be strictly a raw JSON list of objects. No markdown backticks.
    Schema:
    {{
        "day": 1,
        "theme": "Brief title of the day",
        "activities": [
            {{"time": "09:00 AM", "activity": "Name", "description": "Details", "location": "Spot"}},
            {{"time": "02:00 PM", "activity": "Name", "description": "Details", "location": "Spot"}}
        ]
    }}
    """

    try:
        response = model.generate_content(prompt)
        # Sanitizing AI output to ensure clean JSON parsing
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_json)
    except Exception as e:
        print(f"GenAI Error: {e}")
        return None