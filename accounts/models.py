from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    city = models.CharField(max_length=50, choices=settings.DRC_CITIES, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_business_owner = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Profil de {self.user.username}'

    @property
    def review_count(self):
        return self.user.reviews.count()
