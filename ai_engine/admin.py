from django.contrib import admin
from .models import TripPlan


# ============================
# TRIP PLAN ADMIN
# ============================
@admin.register(TripPlan)
class TripPlanAdmin(admin.ModelAdmin):

    # List view (table)
    list_display = (
        'id',
        'user',
        'title',
        'days',
        'interests',
        'created_at',
    )

    # Filters (right sidebar)
    list_filter = (
        'interests',
        'days',
        'created_at',
    )

    # Search capability
    search_fields = (
        'title',
        'user__email',
    )

    # Default ordering
    ordering = ('-created_at',)

    # Read-only fields
    readonly_fields = ('created_at',)

    # Field organization (detail page)
    fieldsets = (
        ("Trip Details", {
            'fields': ('user', 'title', 'days', 'interests')
        }),
        ("AI Generated Itinerary", {
            'fields': ('itinerary_data',)
        }),
        ("Metadata", {
            'fields': ('created_at',)
        }),
    )
