from django.urls import path
from django.contrib.auth import views as auth_views

from destinations import views
from .views import (
    login_view, logout_view, signup_view, verify_otp_view, 
    dashboard_redirect, admin_dashboard, user_dashboard, profile_settings,
    admin_moderation, user_manager_view, toggle_user_status,
    destination_manager, delete_review, manage_services, toggle_service_verification, edit_destination, delete_destination
)

urlpatterns = [
    # --- Core Authentication ---
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('verify-otp/', verify_otp_view, name='verify_otp'),

    # --- Dashboards (Role-Based) ---
    path('dashboard/', dashboard_redirect, name='dashboard'),
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/user/', user_dashboard, name='user_dashboard'),
    path('profile/', profile_settings, name='profile_settings'),

    # --- Admin Governance & Moderation ---
    # Manage platform-wide reviews and sentiment
    path('moderation/', admin_moderation, name='admin_moderation'),
    path('review/delete/<int:review_id>/', delete_review, name='delete_review'),
    
    # Audit registered users and manage account status
    path('users/', user_manager_view, name='user_manager'),
    path('users/toggle/<int:user_id>/', toggle_user_status, name='toggle_user_status'),
    
    # Global destination and service provider management
    path('destinations/manage/', destination_manager, name='destination_manager'),

    path('services/manage/', manage_services, name='manage_services'),
    path('services/verify/<str:service_type>/<int:service_id>/', toggle_service_verification, name='toggle_service_verification'),

    # --- Password Reset Flow ---
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt'
    ), name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),

    path('destinations/edit/<int:dest_id>/',edit_destination, name='edit_destination'),
    path('destinations/delete/<int:dest_id>/', delete_destination, name='delete_destination'),
]