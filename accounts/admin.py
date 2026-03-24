from django.contrib import admin
from .models import Profile, SubscriptionPlan, UserSubscription


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'phone', 'is_business_owner', 'created_at')
    list_filter = ('is_business_owner', 'city')
    search_fields = ('user__username', 'user__email', 'phone')
    readonly_fields = ('created_at',)


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name', 'price_monthly', 'max_photos_per_business', 'max_businesses', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('is_active', 'price_monthly', 'max_photos_per_business', 'max_businesses')


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'status', 'started_at', 'expires_at', 'auto_renew')
    list_filter = ('status', 'plan', 'auto_renew')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('started_at',)
