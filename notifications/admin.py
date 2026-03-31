from django.contrib import admin
from .models import Notification


# ============================
# NOTIFICATION ADMIN
# ============================
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    # List display (main table)
    list_display = (
        'id',
        'user',
        'title',
        'is_read',
        'created_at',
    )

    # Sidebar filters
    list_filter = (
        'is_read',
        'created_at',
    )

    # Search functionality
    search_fields = (
        'title',
        'message',
        'user__email',
    )

    # Default ordering
    ordering = ('-created_at',)

    # Read-only fields
    readonly_fields = ('created_at',)

    # Field grouping
    fieldsets = (
        ("Notification Info", {
            'fields': ('user', 'title', 'message')
        }),
        ("Status", {
            'fields': ('is_read',)
        }),
        ("Metadata", {
            'fields': ('created_at',)
        }),
    )

    # ============================
    # BULK ACTIONS (VERY USEFUL)
    # ============================
    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected as READ"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected as UNREAD"
