from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Business, Category
from .forms import BusinessForm
from reviews.models import Review


def home_view(request):
    categories = Category.objects.all()
    recent_businesses = Business.objects.filter(is_active=True)[:8]
    recent_reviews = Review.objects.select_related('business', 'user').order_by('-created_at')[:6]
    context = {
        'categories': categories,
        'recent_businesses': recent_businesses,
        'recent_reviews': recent_reviews,
    }
    return render(request, 'home.html', context)


def business_list(request):
    businesses = Business.objects.filter(is_active=True)
    query = request.GET.get('q', '')
    city = request.GET.get('ville', '')
    category_slug = request.GET.get('categorie', '')

    if query:
        businesses = businesses.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(address__icontains=query)
        )
    if city:
        businesses = businesses.filter(city=city)
    if category_slug:
        businesses = businesses.filter(category__slug=category_slug)

    paginator = Paginator(businesses, 12)
    page = request.GET.get('page')
    businesses = paginator.get_page(page)

    context = {
        'businesses': businesses,
        'query': query,
        'city': city,
        'category_slug': category_slug,
        'categories': Category.objects.all(),
    }
    return render(request, 'businesses/list.html', context)


def business_detail(request, slug):
    business = get_object_or_404(Business, slug=slug, is_active=True)
    reviews = business.reviews.select_related('user').order_by('-created_at')
    context = {
        'business': business,
        'reviews': reviews,
    }
    return render(request, 'businesses/detail.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    businesses = Business.objects.filter(category=category, is_active=True)
    paginator = Paginator(businesses, 12)
    page = request.GET.get('page')
    businesses = paginator.get_page(page)
    context = {
        'category': category,
        'businesses': businesses,
    }
    return render(request, 'businesses/category.html', context)


@login_required
def business_create(request):
    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.owner = request.user
            business.save()
            messages.success(request, 'Votre entreprise a ete ajoutee avec succes!')
            return redirect(business.get_absolute_url())
    else:
        form = BusinessForm()
    return render(request, 'businesses/create.html', {'form': form})


@login_required
def business_edit(request, slug):
    business = get_object_or_404(Business, slug=slug, owner=request.user)
    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES, instance=business)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entreprise mise a jour avec succes!')
            return redirect(business.get_absolute_url())
    else:
        form = BusinessForm(instance=business)
    return render(request, 'businesses/edit.html', {'form': form, 'business': business})


def search_view(request):
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    results = Business.objects.filter(is_active=True)

    if query:
        results = results.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    if location:
        results = results.filter(
            Q(city__icontains=location) |
            Q(commune__icontains=location) |
            Q(address__icontains=location)
        )

    paginator = Paginator(results, 12)
    page = request.GET.get('page')
    results = paginator.get_page(page)

    context = {
        'results': results,
        'query': query,
        'location': location,
    }
    return render(request, 'businesses/search_results.html', context)
