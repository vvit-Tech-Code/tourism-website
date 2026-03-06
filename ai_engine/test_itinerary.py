import json
from django.test import TestCase
from unittest.mock import patch, MagicMock
from ai_engine.itinerary_service import generate_smart_itinerary

class ItineraryParsingTest(TestCase):
    
    @patch('google.generativeai.GenerativeModel.generate_content')
    def test_generate_smart_itinerary_raw_list(self, mock_generate):
        # Mock Gemini returning a raw list of objects
        mock_response = MagicMock()
        mock_response.text = json.dumps([
            {"day": 1, "theme": "Test Day", "activities": []}
        ])
        mock_generate.return_value = mock_response
        
        result = generate_smart_itinerary(1, 'ECO', 'Karnataka', 'Bengaluru')
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['day'], 1)

    @patch('google.generativeai.GenerativeModel.generate_content')
    def test_generate_smart_itinerary_wrapped_list(self, mock_generate):
        # Mock Gemini returning a wrapped list (common variation)
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "itinerary": [
                {"day": 1, "theme": "Wrapped Day", "activities": []}
            ]
        })
        mock_generate.return_value = mock_response
        
         # We need to configure the model in the test to avoid errors or just mock the entire thing
        result = generate_smart_itinerary(1, 'ECO', 'Karnataka', 'Bengaluru')
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['theme'], "Wrapped Day")

    @patch('google.generativeai.GenerativeModel.generate_content')
    def test_generate_smart_itinerary_error_handling(self, mock_generate):
        # Mock Gemini returning invalid content
        mock_response = MagicMock()
        mock_response.text = "This is not JSON"
        mock_generate.return_value = mock_response
        
        result = generate_smart_itinerary(1, 'ECO', 'Karnataka', 'Bengaluru')
        
        # Should return empty list on parsing failure
        self.assertEqual(result, [])
