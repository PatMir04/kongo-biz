from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings


class Category(models.Model):
    CATEGORY_CHOICES = [
        ('restaurants', 'Restaurants'),
        ('hotels', 'Hotels'),
        ('pharmacies', 'Pharmacies'),
        ('hopitaux', 'Hopitaux & Cliniques'),
        ('ecoles', 'Ecoles & Universites'),
        ('marches', 'Marches'),
        ('transport', 'Transport'),
        ('banques', 'Banques & Finance'),
        ('salons', 'Salons de Beaute'),
        ('auto', 'Reparation Auto'),
        ('technologie', 'Technologie & Telecom'),
        ('immobilier', 'Immobilier'),
        ('juridique', 'Services Juridiques'),
        ('alimentation', 'Alimentation & Boissons'),
        ('divertissement', 'Divertissement'),
    ]

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, default='bi-shop', help_text='Bootstrap icon class')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('businesses:category_detail', kwargs={'slug': self.slug})


class Province(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    city_count = models.PositiveIntegerField(default=0, help_text='Number of cities in this province')

    class Meta:
        ordering = ['name']
        verbose_name = 'Province'
        verbose_name_plural = 'Provinces'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Business(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='businesses')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='businesses')
    description = models.TextField()
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True, related_name='businesses')
    city = models.CharField(max_length=100, blank=True, help_text='City or town within the province')
    address = models.CharField(max_length=300, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Businesses'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Ensure unique slug
            original_slug = self.slug
            counter = 1
            while Business.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('businesses:business_detail', kwargs={'slug': self.slug})

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(r.rating for r in reviews) / len(reviews)
        return 0

    @property
    def review_count(self):
        return self.reviews.count()

    @property
    def location_display(self):
        parts = []
        if self.city:
            parts.append(self.city)
        if self.province:
            parts.append(self.province.name)
        return ', '.join(parts) if parts else ''

    @property
    def photo_count(self):
        return self.photos.count()

    def can_add_photo(self):
        """Check if owner can add more photos based on subscription"""
        from accounts.models import UserSubscription
        try:
            sub = self.owner.subscription
            max_photos = sub.plan.max_photos_per_business
        except (UserSubscription.DoesNotExist, AttributeError):
            max_photos = 3
        return self.photo_count < max_photos

    def max_photos_allowed(self):
        from accounts.models import UserSubscription
        try:
            sub = self.owner.subscription
            return sub.plan.max_photos_per_business
        except (UserSubscription.DoesNotExist, AttributeError):
            return 3


class BusinessPhoto(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='businesses/photos/')
    caption = models.CharField(max_length=200, blank=True, verbose_name='legende')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', '-uploaded_at']
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

    def __str__(self):
        return f"Photo de {self.business.name}"
