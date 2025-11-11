from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_display_name', 'is_seller', 'verification_status', 'average_rating', 'created_at')
    list_filter = ('is_seller', 'verification_status', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at', 'total_sales', 'average_rating')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Profile Details', {
            'fields': ('bio', 'profile_picture', 'phone_number')
        }),
        ('Seller Information', {
            'fields': ('is_seller', 'verification_status')
        }),
        ('Statistics', {
            'fields': ('total_sales', 'average_rating'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_display_name(self, obj):
        return obj.get_display_name()
    get_display_name.short_description = 'Display Name'
