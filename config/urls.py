from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin Site
    path('admin/', admin.site.urls),

    # Services App (Public Landing, About, and Global Services)
    # We map the root '' here so the landing page works immediately
    path('', include('services.urls')),

    # Accounts App (Authentication, User/Admin Dashboards, Profiles)
    path('accounts/', include('accounts.urls')),

    # Destinations App (Explore Map, Place Details, Add Places)
    path('destinations/', include('destinations.urls')),

    # AI Engine App (Trip Planner, Chatbot, Sentiment Analysis API)
    path('ai-engine/', include('ai_engine.urls')),

    # Notifications App (Alerts and Dropdown Logic)
    path('notifications/', include('notifications.urls')), 
]

# CRITICAL: Serving Media and Static files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)