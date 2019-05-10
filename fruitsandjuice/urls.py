from django.urls import path, reverse

from fruitsandjuice.views import (
    ProductListView,
    AboutView,
    ShippayView,
    HomeRedirectView,
)

app_name = 'fruitsandjuice'

urlpatterns = [
    path('', HomeRedirectView.as_view(), name='go_to_index'),
    path('home', ProductListView.as_view(), name='home'),
    path('about', AboutView.as_view(), name='about'),
    path('shippay', ShippayView.as_view(), name='shippay'),
]
