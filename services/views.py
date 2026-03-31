import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from .models import Review
from destinations.models import Destination
from django.contrib.admin.views.decorators import staff_member_required
from notifications.models import Notification 
from ai_engine.logic import analyze_sentiment


# Assuming logic.py exists in ai_engine as created in previous step
try:
    from ai_engine.logic import analyze_sentiment
except ImportError:
    def analyze_sentiment(text): return "NEUTRAL", 0.0

def home(request):
    """Requirement: Homepage Hero section with Dynamic Review Feed."""
    # Pulling the latest 5 reviews that have been analyzed by AI
    latest_reviews = Review.objects.all().order_by('-created_at')[:5]
    
    review_updates = []
    for r in latest_reviews:
        review_updates.append({
            'user': r.user.full_name or r.user.email.split('@')[0],
            'sentiment': r.sentiment.lower(), # positive, neutral, negative
            'place': r.destination.name,
            'text': r.comment[:60] + "..." if len(r.comment) > 60 else r.comment
        })

    # Default if no reviews exist yet
    if not review_updates:
        review_updates = [{'user': 'System', 'sentiment': 'positive', 'place': 'Jharkhand', 'text': 'Welcome to Bharat AI Travel Portal!'}]

    return render(request, 'landing.html', {'review_updates': review_updates})

def destinations_public(request):
    """Public Destinations Overview"""
    places = Destination.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).order_by('-created_at')
    return render(request, 'destinations_pub.html', {'places': places})

def about_vision(request):
    """Project Problem Statement & Vision"""
    return render(request, 'about.html')

@login_required
def submit_review(request, destination_id):
    """
    AI-Powered Review Submission with Automated Notifications.
    Features: ML Sentiment Classification & Real-time User Alerting.
    """
    destination = get_object_or_404(Destination, id=destination_id)
    
    if request.method == 'POST':
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')
        
        if not comment or not rating:
            messages.error(request, "Please provide both a rating and a comment.")
            return render(request, 'services/submit_review.html', {'destination': destination})

        # 1. ML Inference: Classify the feedback using ai_engine
        # Label: POSITIVE/NEUTRAL/NEGATIVE, Score: -1.0 to 1.0
        label, score = analyze_sentiment(comment)
        
        # 2. Database Persistence
        review = Review.objects.create(
            user=request.user,
            destination=destination,
            comment=comment,
            rating=rating,
            sentiment=label,
            sentiment_score=score
        )
        
        # 3. Trigger In-App Notification (Requirement: Notifications)
        # This allows the user to see the "AI Analysis Complete" alert in their sidebar
        Notification.objects.create(
            user=request.user,
            title="Review Analyzed ✨",
            message=f"Your feedback for {destination.name} was classified as {label} by Bharat AI."
        )

        # 4. Success Message and Redirect
        messages.success(request, f"Review submitted successfully! AI Sentiment: {label}")
        return redirect('place_detail', pk=destination.id)
    
    return render(request, 'services/submit_review.html', {'destination': destination})


@staff_member_required
def delete_review(request, pk):
    """Requirement: Review Moderation - Admin can remove content."""
    review = get_object_or_404(Review, pk=pk)
    destination_id = review.destination.id
    review.delete()
    messages.success(request, "Review moderated and successfully removed.")
    return redirect('place_detail', pk=destination_id)

@staff_member_required
def moderate_review(request, review_id):
    """Admin-only: Delete or Hide a review"""
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    messages.success(request, "Review has been moderated and removed.")
    return redirect('admin_dashboard')

def landing_view(request):
    """
    Requirement: Homepage with Dynamic Review Feed.
    Fetches the latest reviews to populate the scrolling ticker.
    """
    # Fetch the latest 5 reviews
    latest_reviews = Review.objects.all().order_by('-created_at')[:5]
    
    review_updates = []
    for r in latest_reviews:
        review_updates.append({
            # Uses full name if available, else part of email
            'user': r.user.full_name or r.user.email.split('@')[0], 
            'sentiment': r.sentiment.lower(), # converted to lower for CSS/Text
            'place': r.destination.name,
            'comment': r.comment[:50] + "..." if len(r.comment) > 50 else r.comment
        })

    # Fallback if no reviews exist yet
    if not review_updates:
        review_updates = [{
            'user': 'System', 
            'sentiment': 'positive', 
            'place': 'Bharat AI', 
            'comment': 'Welcome to the future of smart tourism!'
        }]
    
    return render(request, 'landing.html', {'review_updates': review_updates})