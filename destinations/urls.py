from django.urls import path
from . import views

urlpatterns = [
    path('explore/', views.explore_view, name='destinations_public'),
    path('place/<int:pk>/', views.place_detail_view, name='place_detail'),
    path('map/', views.interactive_map_view, name='map_view'),
    path('add/', views.add_destination, name='add_destination'),
    path('manage-services/', views.manage_services, name='manage_services'),
    path('chatbot/query/', views.chatbot_query, name='chatbot_query'),
    path('itinerary/generate/', views.itinerary_generator, name='itinerary_gen'),
]