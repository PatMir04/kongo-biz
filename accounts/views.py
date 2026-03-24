from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm, ProfileForm
from .models import Profile


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Bienvenue sur KongoBiz!')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Vous avez ete deconnecte.')
    return redirect('home')


@login_required
def profile_view(request, username=None):
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        profile_user = request.user
    profile, created = Profile.objects.get_or_create(user=profile_user)
    reviews = profile_user.reviews.select_related('business').order_by('-created_at')
    businesses = profile_user.businesses.filter(is_active=True)
    context = {
        'profile_user': profile_user,
        'profile': profile,
        'reviews': reviews,
        'businesses': businesses,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis a jour!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile_edit.html', {'form': form})
