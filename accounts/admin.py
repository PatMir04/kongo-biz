from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'phone', 'is_business_owner', 'created_at')
    list_filter = ('is_business_owner', 'city')
    search_fields = ('user__username', 'user__email', 'phone')
    readonly_fields = ('created_at',)
