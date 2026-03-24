from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('inscription/', views.signup_view, name='signup'),
    path('connexion/', views.login_view, name='login'),
    path('deconnexion/', views.logout_view, name='logout'),
    path('profil/', views.profile_view, name='profile'),
    path('profil/modifier/', views.profile_edit, name='profile_edit'),
    path('profil/<str:username>/', views.profile_view, name='user_profile'),
]
