from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_vision, name='about_vision'),
    path('destinations-overview/', views.destinations_public, name='destinations_public'),
    path('submit-review/<int:destination_id>/', views.submit_review, name='submit_review'),
]