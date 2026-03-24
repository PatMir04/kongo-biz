from django.contrib import admin
from .models import Category, Business, BusinessPhoto, Province


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'city_count']
    prepopulated_fields = {'slug': ('name',)}


class BusinessPhotoInline(admin.TabularInline):
    model = BusinessPhoto
    extra = 1
    readonly_fields = ('uploaded_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'province', 'owner', 'is_verified', 'is_active', 'created_at']
    list_filter = ['province', 'category', 'is_verified', 'is_active']
    search_fields = ['name', 'description', 'address']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_verified', 'is_active']
    inlines = [BusinessPhotoInline]


@admin.register(BusinessPhoto)
class BusinessPhotoAdmin(admin.ModelAdmin):
    list_display = ['business', 'caption', 'is_primary', 'uploaded_at']
    list_filter = ['is_primary', 'uploaded_at']
    search_fields = ['business__name', 'caption']
