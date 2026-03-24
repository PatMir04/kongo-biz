from django.contrib import admin
from .models import Category, Business


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'city', 'owner', 'is_verified', 'is_active', 'created_at']
    list_filter = ['city', 'category', 'is_verified', 'is_active']
    search_fields = ['name', 'description', 'address']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_verified', 'is_active']
