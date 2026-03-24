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


class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('free', 'Gratuit'),
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise'),
    ]

    name = models.CharField(max_length=50, choices=PLAN_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    price_monthly = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    max_photos_per_business = models.IntegerField(default=3)
    max_businesses = models.IntegerField(default=1)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['price_monthly']
        verbose_name = 'Plan'
        verbose_name_plural = 'Plans'

    def __str__(self):
        return f'{self.display_name} - ${self.price_monthly}/mois'


class UserSubscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Actif'),
        ('cancelled', 'Annule'),
        ('expired', 'Expire'),
        ('pending', 'En attente'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, related_name='subscribers')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    auto_renew = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Abonnement'
        verbose_name_plural = 'Abonnements'

    def __str__(self):
        return f'{self.user.username} - {self.plan.display_name}'

    @property
    def is_active(self):
        from django.utils import timezone
        if self.status != 'active':
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True
