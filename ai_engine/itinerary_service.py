import json
import google.generativeai as genai
from django.conf import settings

def generate_smart_itinerary(days, category, state, city=""):
    """
    Requirement: AI National Trip Planner.
    Generates a day-wise itinerary for any state in India using Gemini.
    """
    genai.configure(api_key=settings.AI_API_KEY)
    # Using the validated 2.5 Lite model as used in chatbot_query
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    
    location = f"{city}, {state}" if city else state
    
    # System prompt forces Gemini to act as a structured data provider
    prompt = f"""
    Act as a professional Indian travel consultant. 
    Generate a detailed {days}-day itinerary for {location}, India.
    Current Focus/Theme: {category} (e.g., Eco-Tourism, Cultural Heritage, Adventure).
    
    Return the result ONLY as a JSON list of objects representing each day.
    
    Required JSON Schema for each object:
    {{
        "day": 1,
        "theme": "Title for this day",
        "activities": [
            {{
                "time": "HH:MM AM/PM",
                "activity": "Activity name",
                "description": "Short description of what to do",
                "location": "Specific spot name"
            }}
        ]
    }}
    
    Ensure all values are strings. Output exactly {days} days.
    """

    try:
        # Use generation_config to ensure valid JSON
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        # Parse the JSON response
        data = json.loads(response.text)
        
        # If Gemini wraps the list in an object (e.g. {"itinerary": [...]}), try to extract it
        if isinstance(data, dict):
            # Check for common keys
            for key in ['itinerary', 'days', 'plan', 'itinerary_data']:
                if key in data and isinstance(data[key], list):
                    return data[key]
            # If it's a single object that looks like a day, wrap it in a list
            if 'day' in data and 'activities' in data:
                return [data]
        
        return data if isinstance(data, list) else []
        
    except Exception as e:
        print(f"GenAI Error in generate_smart_itinerary: {e}")
        return []