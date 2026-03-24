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
]
