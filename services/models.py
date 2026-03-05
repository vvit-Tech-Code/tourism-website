from django.db import models
from django.conf import settings
from destinations.models import Destination

class Review(models.Model):
    SENTIMENT_CHOICES = [
        ('POSITIVE', 'Positive'),
        ('NEUTRAL', 'Neutral'),
        ('NEGATIVE', 'Negative'),
        ('PENDING', 'Pending Analysis'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    
    # AI Sentiment Fields
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES, default='PENDING')
    sentiment_score = models.FloatField(default=0.0) # For confidence levels
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.destination.name} ({self.sentiment})"