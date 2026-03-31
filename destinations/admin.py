from django.contrib import admin
from .models import (
    ChatConversation,
    Itinerary,
    Destination,
    LocalGuide,
    Homestay
)
import json
from django.utils.html import format_html


# ============================
# CHAT CONVERSATION ADMIN
# ============================
@admin.register(ChatConversation)
class ChatConversationAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'is_anonymous',
        'short_message',
        'timestamp',
    )

    list_filter = (
        'is_anonymous',
        'timestamp',
    )

    search_fields = (
        'user__email',
        'message',
        'response',
    )

    ordering = ('-timestamp',)

    readonly_fields = ('timestamp',)

    def short_message(self, obj):
        return obj.message[:50]
    short_message.short_description = "Message"


# ============================
# ITINERARY ADMIN
# ============================
@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'title',
        'days',
        'created_at',
    )

    list_filter = (
        'days',
        'created_at',
    )

    search_fields = (
        'title',
        'user__email',
    )

    ordering = ('-created_at',)

    readonly_fields = ('created_at', 'formatted_plan')

    def formatted_plan(self, obj):
        return format_html(
            "<pre style='white-space: pre-wrap;'>{}</pre>",
            json.dumps(obj.plan_data, indent=2)
        )

    formatted_plan.short_description = "Plan (Formatted)"

    fieldsets = (
        ("Trip Info", {
            'fields': ('user', 'title', 'days', 'interests')
        }),
        ("AI Plan", {
            'fields': ('formatted_plan',)
        }),
        ("Metadata", {
            'fields': ('created_at',)
        }),
    )


# ============================
# LOCAL GUIDE INLINE
# ============================
class LocalGuideInline(admin.TabularInline):
    model = LocalGuide
    extra = 1


# ============================
# HOMESTAY INLINE
# ============================
class HomestayInline(admin.TabularInline):
    model = Homestay
    extra = 1


# ============================
# DESTINATION ADMIN
# ============================
@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'state',
        'category',
        'best_time',
        'created_at',
    )

    list_filter = (
        'category',
        'state',
    )

    search_fields = (
        'name',
        'state',
        'description',
    )

    ordering = ('-created_at',)

    readonly_fields = ('created_at', 'image_preview')

    inlines = [LocalGuideInline, HomestayInline]

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="120" style="border-radius:10px;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Preview"

    fieldsets = (
        ("Basic Info", {
            'fields': ('name', 'state', 'category')
        }),
        ("Content", {
            'fields': ('description', 'history')
        }),
        ("Location", {
            'fields': ('latitude', 'longitude')
        }),
        ("Media", {
            'fields': ('image', 'image_preview')
        }),
        ("Visiting Info", {
            'fields': ('best_time', 'visiting_time')
        }),
        ("Metadata", {
            'fields': ('created_at',)
        }),
    )


# ============================
# LOCAL GUIDE ADMIN
# ============================
@admin.register(LocalGuide)
class LocalGuideAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'destination',
        'languages',
        'fee',
        'is_verified',
    )

    list_filter = (
        'is_verified',
        'destination',
    )

    search_fields = (
        'name',
        'destination__name',
    )


# ============================
# HOMESTAY ADMIN
# ============================
@admin.register(Homestay)
class HomestayAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'destination',
        'price_per_night',
        'is_verified',
    )

    list_filter = (
        'is_verified',
        'destination',
    )

    search_fields = (
        'name',
        'destination__name',
    )
