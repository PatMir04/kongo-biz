from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from businesses.models import Business
from .models import Review
from .forms import ReviewForm


@login_required
def add_review(request, slug):
    business = get_object_or_404(Business, slug=slug, is_active=True)
    existing_review = Review.objects.filter(
        business=business, user=request.user
    ).first()

    if existing_review:
        messages.warning(request, 'Vous avez deja laisse un avis pour cette entreprise.')
        return redirect('businesses:detail', slug=slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.business = business
            review.user = request.user
            review.save()
            messages.success(request, 'Votre avis a ete ajoute avec succes!')
            return redirect('businesses:detail', slug=slug)
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'business': business,
    }
    return render(request, 'reviews/add_review.html', context)


@login_required
def edit_review(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre avis a ete mis a jour!')
            return redirect('businesses:detail', slug=review.business.slug)
    else:
        form = ReviewForm(instance=review)

    context = {
        'form': form,
        'review': review,
        'business': review.business,
    }
    return render(request, 'reviews/edit_review.html', context)


@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)
    business_slug = review.business.slug

    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Votre avis a ete supprime.')
        return redirect('businesses:detail', slug=business_slug)

    return render(request, 'reviews/delete_review.html', {
        'review': review
    })
