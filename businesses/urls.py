from django.urls import path
from . import views

app_name = 'businesses'

urlpatterns = [
    path('', views.business_list, name='list'),
    path('recherche/', views.search_view, name='search'),
    path('ajouter/', views.business_create, name='create'),
    path('categorie/<slug:slug>/', views.category_detail, name='category_detail'),
    path('<slug:slug>/', views.business_detail, name='detail'),
    path('<slug:slug>/modifier/', views.business_edit, name='edit'),
    path('<slug:slug>/ajouter-photo/', views.add_photo, name='add_photo'),
    path('<slug:slug>/signaler/', views.flag_business, name='flag_business'),
    path('photo/<int:photo_id>/supprimer/', views.delete_photo, name='delete_photo'),
]
