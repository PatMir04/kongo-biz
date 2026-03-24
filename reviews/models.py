from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from businesses.models import Business


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Mauvais'),
        (2, '2 - Mediocre'),
        (3, '3 - Moyen'),
        (4, '4 - Bon'),
        (5, '5 - Excellent'),
    ]

    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name='reviews'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=RATING_CHOICES
    )
    comment = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['business', 'user']
        verbose_name = 'Avis'
        verbose_name_plural = 'Avis'

    def __str__(self):
        return f'{self.user.username} - {self.business.name} ({self.rating}/5)'


class ReviewFlag(models.Model):
    FLAG_REASONS = [
        ('spam', 'Spam ou contenu inapproprie'),
        ('fake', 'Avis faux ou trompeur'),
        ('offensive', 'Contenu offensant'),
        ('irrelevant', 'Non pertinent'),
        ('other', 'Autre'),
    ]

    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('reviewed', 'Examine'),
        ('dismissed', 'Rejete'),
        ('removed', 'Supprime'),
    ]

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='flags'
    )
    flagged_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review_flags'
    )
    reason = models.CharField(max_length=20, choices=FLAG_REASONS)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='resolved_flags'
    )

    class Meta:
        unique_together = ['review', 'flagged_by']
        ordering = ['-created_at']
        verbose_name = 'Signalement'
        verbose_name_plural = 'Signalements'

    def __str__(self):
        return f'Flag on {self.review} by {self.flagged_by.username}'


class BusinessFlag(models.Model):
    FLAG_REASONS = [
        ('fake', 'Entreprise fausse ou inexistante'),
        ('duplicate', 'Doublon'),
        ('closed', 'Entreprise fermee'),
        ('misleading', 'Informations trompeuses'),
        ('other', 'Autre'),
    ]

    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('reviewed', 'Examine'),
        ('dismissed', 'Rejete'),
        ('removed', 'Supprime'),
    ]

    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name='flags'
    )
    flagged_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='business_flags'
    )
    reason = models.CharField(max_length=20, choices=FLAG_REASONS)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='resolved_business_flags'
    )

    class Meta:
        unique_together = ['business', 'flagged_by']
        ordering = ['-created_at']
        verbose_name = 'Signalement Entreprise'
        verbose_name_plural = 'Signalements Entreprises'

    def __str__(self):
        return f'Flag on {self.business.name} by {self.flagged_by.username}'
