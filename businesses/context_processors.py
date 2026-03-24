from .models import Category, Province


def categories_processor(request):
    return {
        'nav_categories': Category.objects.all(),
        'nav_provinces': Province.objects.all(),
    }
