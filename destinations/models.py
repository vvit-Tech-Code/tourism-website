from django.db import models
from django.conf import settings

# --- AI & SYSTEM LOGS ---

class ChatConversation(models.Model):
    """Logs for the AI Travel Assistant (Chatbot)"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    response = models.TextField()
    is_anonymous = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'Anonymous' if self.is_anonymous else self.user.email} | {self.timestamp}"

class Itinerary(models.Model):
    """Stores the AI-generated JSON travel plans for History tracking"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_itineraries')
    title = models.CharField(max_length=200, default="My India Trip")
    days = models.IntegerField()
    interests = models.TextField()
    plan_data = models.JSONField() # Stores the AI-generated JSON array
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.days} Days"


# --- INFRASTRUCTURE MODELS ---

class Destination(models.Model):
    """Primary Tourism Node (National Scope)"""
    CATEGORY_CHOICES = [
        ('ECO', 'Eco-Tourism'),
        ('CULTURAL', 'Cultural Heritage'),
    ]

    name = models.CharField(max_length=200)
    state = models.CharField(max_length=100, default="Jharkhand") 
    description = models.TextField()
    history = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    # Geolocation for Google Maps API
    latitude = models.FloatField(default=23.3441)
    longitude = models.FloatField(default=85.3096)
    
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    best_time = models.CharField(max_length=100, default="October to March")
    visiting_time = models.CharField(max_length=100, blank=True, null=True, default="9:00 AM - 6:00 PM")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class LocalGuide(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='guides')
    name = models.CharField(max_length=100)
    # Added a default value so migrations never get stuck
    phone = models.CharField(max_length=20, default="0000000000") 
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    languages = models.CharField(max_length=200, default="Hindi, English")
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    is_verified = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.destination.name})"

class Homestay(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='homestays')
    name = models.CharField(max_length=200)
    # Added a default value here as well
    contact = models.CharField(max_length=20, default="Not Provided") 
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    amenities = models.TextField(default="WiFi, Local Food, Parking")
    is_verified = models.BooleanField(default=True)

    def __str__(self):
        return self.name