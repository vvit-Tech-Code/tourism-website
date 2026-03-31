from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notification

@login_required
def notifications_list(request):
    """
    Displays all notifications for the logged-in user.
    Updates all unread notifications to 'read' upon viewing.
    """
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Logic to mark all as read automatically when page is opened
    unread_notes = notifications.filter(is_read=False)
    if unread_notes.exists():
        unread_notes.update(is_read=True)
        
    return render(request, 'notifications/list.html', {
        'notifications': notifications
    })

@login_required
def mark_as_read(request, pk):
    """
    Action to mark a single specific notification as read.
    """
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications_list')

@login_required
def delete_notification(request, pk):
    """
    Allows users to dismiss/delete a notification.
    """
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.delete()
    messages.success(request, "Notification dismissed.")
    return redirect('notifications_list')