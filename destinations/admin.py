from django.contrib import admin
from .models import Destination, LocalGuide, Homestay

class GuideInline(admin.TabularInline):
    model = LocalGuide
    extra = 1

class HomestayInline(admin.TabularInline):
    model = Homestay
    extra = 1

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'best_time')
    search_fields = ('name',)
    inlines = [GuideInline, HomestayInline]