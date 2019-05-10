from django.db.models import OuterRef, Subquery
from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView, ListView
from django.urls import reverse
from fruitsandjuice.models import Product, ProductImages, ProductCategory

# Create your views here.

class HomeRedirectView(RedirectView):

    permanent = False
    query_string = True
    pattern_name = 'article-detail'

    def get_redirect_url(self, *args, **kwargs):
        return reverse('fruitsandjuice:home')

class ProductListView(ListView):
    model = Product
    template_name = 'fruitandjuice/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = Product.objects.all()
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AboutView(TemplateView):
    template_name = 'fruitandjuice/about.html'

class ShippayView(TemplateView):
    template_name = 'fruitandjuice/shippay.html'
