from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, EmailOTP


# ============================
# CUSTOM USER ADMIN
# ============================
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    # Display in admin list
    list_display = (
        'email',
        'full_name',
        'role',
        'is_verified',
        'is_staff',
        'is_active',
        'login_count',
    )

    # Filters
    list_filter = (
        'role',
        'is_verified',
        'is_staff',
        'is_active',
    )

    # Search
    search_fields = ('email', 'full_name', 'phone_number')

    ordering = ('-id',)

    # Remove username field completely
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {
            'fields': ('full_name', 'phone_number', 'profile_picture')
        }),
        ('Roles & Permissions', {
            'fields': (
                'role',
                'is_verified',
                'is_staff',
                'is_active',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Activity', {'fields': ('last_login', 'login_count')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'role',
                'is_verified',
                'is_staff',
                'is_active',
            ),
        }),
    )

    readonly_fields = ('last_login',)


# ============================
# EMAIL OTP ADMIN
# ============================
@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'created_at', 'is_valid')
    search_fields = ('user__email', 'otp')
    readonly_fields = ('created_at',)

    def is_valid(self, obj):
        return not obj.is_expired()

    is_valid.boolean = True
    is_valid.short_description = "OTP Valid"
