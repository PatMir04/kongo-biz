from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Business, Category, BusinessPhoto, Province
from .forms import BusinessForm, BusinessPhotoForm
from reviews.models import Review
from reviews.models import BusinessFlag
from reviews.forms import BusinessFlagForm


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
    province_id = request.GET.get('province', '')
    category_slug = request.GET.get('categorie', '')

    if query:
        businesses = businesses.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(address__icontains=query)
        )
    if province_id:
        businesses = businesses.filter(province_id=province_id)
    if category_slug:
        businesses = businesses.filter(category__slug=category_slug)

    paginator = Paginator(businesses, 12)
    page = request.GET.get('page')
    businesses = paginator.get_page(page)

    context = {
        'businesses': businesses,
        'query': query,
        'province_id': province_id,
        'category_slug': category_slug,
        'categories': Category.objects.all(),
        'provinces': Province.objects.all(),
    }
    return render(request, 'businesses/list.html', context)


def business_detail(request, slug):
    business = get_object_or_404(Business, slug=slug, is_active=True)
    reviews = business.reviews.select_related('user').order_by('-created_at')
    photos = business.photos.all()
    can_add_photo = False
    if request.user.is_authenticated and request.user == business.owner:
        can_add_photo = business.can_add_photo()
    context = {
        'business': business,
        'reviews': reviews,
        'photos': photos,
        'can_add_photo': can_add_photo,
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


@login_required
def add_photo(request, slug):
    business = get_object_or_404(Business, slug=slug, owner=request.user)
    if not business.can_add_photo():
        messages.error(request, f'Limite de photos atteinte ({business.max_photos_allowed()} photos). Passez a un plan superieur pour en ajouter plus.')
        return redirect(business.get_absolute_url())
    if request.method == 'POST':
        form = BusinessPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = BusinessPhoto(
                business=business,
                image=request.FILES['image'],
                caption=form.cleaned_data.get('caption', ''),
                is_primary=form.cleaned_data.get('is_primary', False)
            )
            if photo.is_primary:
                business.photos.filter(is_primary=True).update(is_primary=False)
            photo.save()
            messages.success(request, 'Photo ajoutee avec succes!')
            return redirect(business.get_absolute_url())
    else:
        form = BusinessPhotoForm()
    return render(request, 'businesses/add_photo.html', {'form': form, 'business': business})


@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(BusinessPhoto, id=photo_id, business__owner=request.user)
    business = photo.business
    if request.method == 'POST':
        photo.delete()
        messages.success(request, 'Photo supprimee.')
    return redirect(business.get_absolute_url())


@login_required
def flag_business(request, slug):
    business = get_object_or_404(Business, slug=slug)
    if BusinessFlag.objects.filter(business=business, flagged_by=request.user).exists():
        messages.warning(request, 'Vous avez deja signale cette entreprise.')
        return redirect(business.get_absolute_url())
    if request.method == 'POST':
        form = BusinessFlagForm(request.POST)
        if form.is_valid():
            flag = form.save(commit=False)
            flag.business = business
            flag.flagged_by = request.user
            flag.save()
            messages.success(request, 'Merci pour votre signalement. Nous allons examiner cette entreprise.')
            return redirect(business.get_absolute_url())
    else:
        form = BusinessFlagForm()
    return render(request, 'businesses/flag_business.html', {'form': form, 'business': business})


def search_view(request):
    query = request.GET.get('q', '')
    province_id = request.GET.get('province', '')
    results = Business.objects.filter(is_active=True)

    if query:
        results = results.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    if province_id:
        results = results.filter(province_id=province_id)

    paginator = Paginator(results, 12)
    page = request.GET.get('page')
    results = paginator.get_page(page)

    context = {
        'results': results,
        'query': query,
        'province_id': province_id,
        'provinces': Province.objects.all(),
    }
    return render(request, 'businesses/search_results.html', context)
