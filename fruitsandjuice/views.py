from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.


class ProductListView(TemplateView):
    template_name = 'fruitandjuice/home.html'


class AboutView(TemplateView):
    template_name = 'fruitandjuice/about.html'

class ShippayView(TemplateView):
    template_name = 'fruitandjuice/shippay.html'
