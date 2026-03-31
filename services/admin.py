from django.contrib import admin
from .models import Review


# ============================
# REVIEW ADMIN
# ============================
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    # List display
    list_display = (
        'id',
        'user',
        'destination',
        'rating',
        'sentiment',
        'sentiment_score',
        'created_at',
    )

    # Filters
    list_filter = (
        'sentiment',
        'rating',
        'created_at',
        'destination',
    )

    # Search
    search_fields = (
        'user__email',
        'destination__name',
        'comment',
    )

    # Ordering
    ordering = ('-created_at',)

    # Read-only fields
    readonly_fields = ('created_at',)

    # Structured layout
    fieldsets = (
        ("User Review", {
            'fields': ('user', 'destination', 'rating', 'comment')
        }),
        ("AI Sentiment Analysis", {
            'fields': ('sentiment', 'sentiment_score')
        }),
        ("Metadata", {
            'fields': ('created_at',)
        }),
    )

    # ============================
    # BULK ACTIONS (POWERFUL)
    # ============================
    actions = [
        'mark_positive',
        'mark_neutral',
        'mark_negative',
    ]

    def mark_positive(self, request, queryset):
        queryset.update(sentiment='POSITIVE')
    mark_positive.short_description = "Mark selected as POSITIVE"

    def mark_neutral(self, request, queryset):
        queryset.update(sentiment='NEUTRAL')
    mark_neutral.short_description = "Mark selected as NEUTRAL"

    def mark_negative(self, request, queryset):
        queryset.update(sentiment='NEGATIVE')
    mark_negative.short_description = "Mark selected as NEGATIVE"
