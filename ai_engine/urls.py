from django.urls import path
from . import views

urlpatterns = [
    path('planner/', views.trip_planner_view, name='trip_planner'),
    path('history/', views.trip_history_view, name='trip_history'),
    # New detail path using the plan's database ID
    path('history/<int:plan_id>/', views.trip_detail_view, name='trip_detail'),
    path('assistant/', views.chatbot_view, name='ai_assistant'),
    path('assistant/query/', views.chatbot_query, name='chatbot_query'),
]