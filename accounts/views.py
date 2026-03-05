import json
import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Sum
from django.conf import settings

# Entity Imports
from accounts.models import User, EmailOTP
from destinations.models import Destination, LocalGuide, Homestay
from services.models import Review
from notifications.models import Notification
from ai_engine.models import TripPlan


User = get_user_model()

# --- AUTHENTICATION FLOW ---

def login_view(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard' if request.user.role == 'admin' else 'user_dashboard')

    if request.method == 'POST':
        email = request.POST.get('username')  
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user:
            if not user.is_active:
                messages.error(request, 'Account not active. Please verify your email.')
                request.session['verify_user'] = user.id
                return redirect('verify_otp')

            login(request, user)
            user.login_count += 1
            user.save(update_fields=['login_count'])
            return redirect('admin_dashboard' if user.role == 'admin' else 'user_dashboard')

        messages.error(request, 'Invalid credentials. Access Denied.')
    return render(request, 'accounts/login.html')

def signup_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role', 'tourist')

        if User.objects.filter(email=email).exists():
            messages.info(request, 'An account with this email already exists.')
            return redirect('login')

        user = User.objects.create_user(email=email, password=password, role=role, full_name=full_name, is_active=False)
        otp = str(random.randint(100000, 999999))
        EmailOTP.objects.update_or_create(user=user, defaults={'otp': otp})

        try:
            send_mail(
                'Verify Your Bharat AI Account',
                f'Your secure OTP for Bharat AI is {otp}. Valid for 10 minutes.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            request.session['verify_user'] = user.id
            return redirect('verify_otp')
        except Exception:
            user.delete()
            messages.error(request, 'Mail service error. Registration failed.')
            return redirect('signup')
    return render(request, 'accounts/signup.html')

def verify_otp_view(request):
    user_id = request.session.get('verify_user')
    if not user_id: return redirect('signup')
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        otp_obj = EmailOTP.objects.filter(user=user).first()

        if otp_obj and not otp_obj.is_expired() and otp_obj.otp == entered_otp:
            user.is_active = True
            user.is_verified = True
            user.save()
            otp_obj.delete()
            del request.session['verify_user']
            return render(request, 'accounts/verify_success.html')
        
        messages.error(request, 'Invalid or expired token.')
        return render(request, 'accounts/verify_failed.html')
    return render(request, 'accounts/verify_otp.html')

# --- DASHBOARD LOGIC ---

@login_required
def user_dashboard(request):
    """
    Fully Dynamic Tourist Portal Logic.
    Requirement: Personalized greeting, stats, and AI-ranked recommendations.
    """
    # 1. Real-time User Stats
    user_reviews = Review.objects.filter(user=request.user)
    trip_plans_count = TripPlan.objects.filter(user=request.user).count()
    # Count only unread notifications for the 'LIVE' badge feel
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False).count()
    
    # 2. Smart Recommendation Logic (AI Feature)
    # Requirement: Ranking system based on ratings and sentiment scores
    # We fetch a destination that has a high average sentiment
    rec_place = Destination.objects.annotate(
        avg_s=Avg('reviews__sentiment_score')
    ).order_by('-avg_s', '?').first()

    # 3. Recent Notifications for the sidebar card
    recent_notes = Notification.objects.filter(user=request.user).order_by('-created_at')[:3]

    context = {
        'full_name': request.user.full_name or "Bharat Traveler",
        'review_count': user_reviews.count(),
        'plan_count': trip_plans_count,
        'unread_count': unread_notifications,
        'rec_place': rec_place,
        'recent_notes': recent_notes,
    }
    return render(request, 'accounts/user_dashboard.html', context)

@login_required
def admin_dashboard(request):
    """Authority Command Center: Global metrics for verified tourism governance."""
    if request.user.role != 'admin': 
        return redirect('user_dashboard')
    
    # 1. Global Sentiment Analytics
    # Map -1/1 scale to 0-100% for a user-friendly metric
    avg_sentiment = Review.objects.aggregate(Avg('sentiment_score'))['sentiment_score__avg'] or 0
    sentiment_pct = round((avg_sentiment + 1) * 50, 1)
    
    # 2. Top-Performing Destinations based on AI Ranking
    top_destinations = Destination.objects.annotate(
        avg_s=Avg('reviews__sentiment_score'),
        r_count=Count('reviews')
    ).order_by('-avg_s')[:5]

    # 3. System Statistics
    context = {
        'total_users': User.objects.count(),
        'verified_users': User.objects.filter(is_verified=True).count(),
        
        # CHANGE THIS LINE to match your HTML variable:
        'active_places_count': Destination.objects.count(), 
        
        'avg_sentiment_pct': sentiment_pct,
        'top_destinations': top_destinations,
        'guides_count': LocalGuide.objects.filter(is_verified=True).count(),
        'homestays_count': Homestay.objects.count(),
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
def dashboard_redirect(request):
    """Bridge view to route users to their respective dashboards based on role."""
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    return redirect('user_dashboard')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Session ended securely.')
    return redirect('login')

@login_required
def profile_settings(request):
    if request.method == 'POST':
        user = request.user
        user.full_name = request.POST.get('full_name')
        user.phone_number = request.POST.get('phone_number')
        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES.get('profile_picture')
        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('profile_settings')
    return render(request, 'accounts/profile.html')

@login_required
def admin_moderation(request):
    """Audit and moderate reviews to ensure content authenticity."""
    if request.user.role != 'admin':
        return redirect('user_dashboard')
    
    # Fetch all reviews across the system
    reviews = Review.objects.select_related('user', 'destination').all().order_by('-created_at')
    return render(request, 'accounts/admin_moderation.html', {'reviews': reviews})


@login_required
def user_manager_view(request):
    """Audit registered tourists and manage their status."""
    if request.user.role != 'admin':
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
    messages.success(request, f"User status updated.")
    return redirect('user_manager')

@login_required
def destination_manager(request):
    """Manage all tourist spots and their linked service providers."""
    if request.user.role != 'admin':
        return redirect('user_dashboard')
        
    destinations = Destination.objects.all().order_by('name')
    return render(request, 'accounts/destination_manager.html', {'destinations': destinations})

@login_required
def add_destination(request):
    """Manual entry for new tourist spots with image upload support."""
    if request.user.role != 'admin':
        messages.warning(request, "Access Denied. Admin authority required.")
        return redirect('user_dashboard')

    if request.method == 'POST':
        name = request.POST.get('name')
        state = request.POST.get('state', 'Jharkhand')
        category = request.POST.get('category')
        visiting_time = request.POST.get('visiting_time')
        description = request.POST.get('description')
        history = request.POST.get('history', '')
        image = request.FILES.get('image')

        Destination.objects.create(
            name=name,
            state=state,
            category=category,
            visiting_time=visiting_time,
            description=description,
            history=history,
            image=image
        )
        messages.success(request, "New destination added to Bharat AI.")
        return redirect('destination_manager')
        
    return render(request, 'accounts/destination_manager.html')

@login_required
def edit_destination(request, dest_id):
    if request.user.role != 'admin':
        return redirect('user_dashboard')
    
    destination = get_object_or_404(Destination, id=dest_id)
    
    if request.method == 'POST':
        destination.name = request.POST.get('name')
        destination.state = request.POST.get('state')
        destination.category = request.POST.get('category')
        destination.visiting_time = request.POST.get('visiting_time')
        destination.description = request.POST.get('description')
        
        if request.FILES.get('image'):
            destination.image = request.FILES.get('image')
            
        destination.save()
        messages.success(request, f"Platform data for {destination.name} updated.")
        return redirect('destination_manager')

    return render(request, 'accounts/edit_destination.html', {'destination': destination})

@login_required
def delete_destination(request, dest_id):
    """Admin-only: Permanent removal of infrastructure."""
    if request.user.role != 'admin' or request.method != 'POST':
        return redirect('destination_manager')
    
    destination = get_object_or_404(Destination, id=dest_id)
    name = destination.name
    destination.delete()
    messages.warning(request, f"Destination '{name}' has been decommissioned.")
    return redirect('destination_manager')


@login_required
def delete_review(request, review_id):
    """Administrator Command: Securely remove review and update global metrics."""
    if request.user.role != 'admin':
        return redirect('user_dashboard')
    
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    
    # Optional: Send notification to user about moderation
    messages.success(request, "Review moderated and removed successfully.")
    return redirect('admin_moderation')

@login_required
def manage_services(request):
    if request.user.role != 'admin':
        return redirect('user_dashboard')
    
    # Handle Form Submission
    if request.method == 'POST':
        service_type = request.POST.get('service_type')
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        dest_id = request.POST.get('destination')
        destination = get_object_or_404(Destination, id=dest_id)

        if service_type == 'guide':
            LocalGuide.objects.create(
                name=name, 
                phone=contact, # Ensure this matches your model field
                destination=destination, 
                is_verified=True
            )
        elif service_type == 'homestay':
            Homestay.objects.create(
                name=name, 
                contact=contact, 
                destination=destination, 
                is_verified=True
            )
        
        messages.success(request, f"New {service_type} attached to {destination.name} successfully!")
        return redirect('manage_services')

    # Data for the page
    context = {
        'guides': LocalGuide.objects.all().select_related('destination'),
        'homestays': Homestay.objects.all().select_related('destination'),
        'destinations': Destination.objects.all(),
    }
    return render(request, 'accounts/manage_services.html', context)


@login_required
def toggle_service_verification(request, service_type, service_id):
    """
    Admin-only: Manually verify or revoke a service provider's status.
    """
    if request.user.role != 'admin':
        return redirect('user_dashboard')
        
    if service_type == 'guide':
        service = get_object_or_404(LocalGuide, id=service_id)
    else:
        service = get_object_or_404(Homestay, id=service_id)
        
    service.is_verified = not service.is_verified
    service.save()
    
    status = "Verified" if service.is_verified else "Revoked"
    messages.success(request, f"Status for {service.name} updated to {status}.")
    return redirect('manage_services')