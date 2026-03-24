#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py makemigrations businesses accounts reviews
python manage.py migrate

# Seed categories and make PatMir superuser
python manage.py shell << 'SEED'
from businesses.models import Category
from django.contrib.auth import get_user_model
User = get_user_model()
cats = ['Restaurants','Hotels','Pharmacies','Hopitaux & Cliniques','Ecoles & Universites','Marches','Transport','Banques & Finance','Salons de Beaute','Reparation Auto','Technologie & Telecom','Immobilier','Services Juridiques','Alimentation & Boissons','Divertissement']
for c in cats:
    Category.objects.get_or_create(name=c)
print(f'Categories: {Category.objects.count()}')
try:
    u = User.objects.get(username='PatMir')
    u.is_staff = True
    u.is_superuser = True
    u.save()
    print('PatMir is now superuser')
except User.DoesNotExist:
    print('PatMir not found')
SEED
