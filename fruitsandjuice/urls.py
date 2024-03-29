from django.urls import path, re_path

from fruitsandjuice.views import (
    ProductListView,
    AboutView,
    ShippayView,
    HomeRedirectView,
    RegistrationView,
    RegistrationSucessView,
    CartView,
    activate,
    OrderView,
    ProfileView,
    OrderSuccessfulView,
    logout, login_view, AddCartView, RemoveCartItemView)

app_name = 'fruitsandjuice'

urlpatterns = [
    path('', HomeRedirectView.as_view(), name='go_to_index'),
    path('logout/', logout, name='logout'),
    path('login/', login_view, name='login'),
    path('home/', ProductListView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('shippay/', ShippayView.as_view(), name='shippay'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddCartView.as_view(), name='add_cart'),
    path('cart/remove/', RemoveCartItemView.as_view(), name='remove_cart'),
    path('order/<int:pk>/', OrderView.as_view(), name='order'),
    path('order_success/<int:pk>/', OrderSuccessfulView.as_view(), name='order_success'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('sucess_registration/', RegistrationSucessView.as_view(), name='success_registration'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            activate, name='activate')
]
