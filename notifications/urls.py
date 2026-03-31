from django.urls import path
from . import views

urlpatterns = [
    path('', views.notifications_list, name='notifications_list'),
    path('mark-read/<int:pk>/', views.mark_as_read, name='mark_notification_read'),
    path('delete/<int:pk>/', views.delete_notification, name='delete_notification'),
]