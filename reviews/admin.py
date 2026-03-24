from django.contrib import admin
from .models import Review, ReviewFlag, BusinessFlag


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'business', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'business__name', 'comment')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ReviewFlag)
class ReviewFlagAdmin(admin.ModelAdmin):
    list_display = ('review', 'flagged_by', 'reason', 'status', 'created_at')
    list_filter = ('status', 'reason', 'created_at')
    search_fields = ('review__comment', 'flagged_by__username', 'description')
    readonly_fields = ('created_at',)
    actions = ['mark_reviewed', 'mark_dismissed', 'mark_removed']

    def mark_reviewed(self, request, queryset):
        queryset.update(status='reviewed')
    mark_reviewed.short_description = 'Marquer comme examine'

    def mark_dismissed(self, request, queryset):
        queryset.update(status='dismissed')
    mark_dismissed.short_description = 'Rejeter les signalements'

    def mark_removed(self, request, queryset):
        queryset.update(status='removed')
    mark_removed.short_description = 'Supprimer le contenu signale'


@admin.register(BusinessFlag)
class BusinessFlagAdmin(admin.ModelAdmin):
    list_display = ('business', 'flagged_by', 'reason', 'status', 'created_at')
    list_filter = ('status', 'reason', 'created_at')
    search_fields = ('business__name', 'flagged_by__username', 'description')
    readonly_fields = ('created_at',)
    actions = ['mark_reviewed', 'mark_dismissed', 'mark_removed']

    def mark_reviewed(self, request, queryset):
        queryset.update(status='reviewed')
    mark_reviewed.short_description = 'Marquer comme examine'

    def mark_dismissed(self, request, queryset):
        queryset.update(status='dismissed')
    mark_dismissed.short_description = 'Rejeter les signalements'

    def mark_removed(self, request, queryset):
        queryset.update(status='removed')
    mark_removed.short_description = 'Supprimer le contenu signale'
