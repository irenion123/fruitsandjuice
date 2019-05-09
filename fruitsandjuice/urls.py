from django.urls import path

from fruitsandjuice.views import (
    ProductListView,
    AboutView,
    ShippayView,
)

app_name = 'fruitsandjuice'

urlpatterns = [
    path('', ProductListView.as_view(), name='home' ),
    path('about', AboutView.as_view(), name='about' ),
    path('shippay', ShippayView.as_view(), name='shippay' ),
]