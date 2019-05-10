from fruitsandjuice.models import ProductCategory


def categories_menu(request):
    return {
        'categories_menu': ProductCategory.objects.all(),
    }
