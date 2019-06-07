from fruitsandjuice.models import ProductCategory, OrderItem, Order, StatusChoice


def categories_menu(request):
    return {
        'categories_menu': ProductCategory.objects.all(),
    }


def cart_count(request):
    items_count = OrderItem.objects.filter(order__user_name=request.user, order__status=StatusChoice.FM.name).count()
    return {'cart_count': items_count}
