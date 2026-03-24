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
