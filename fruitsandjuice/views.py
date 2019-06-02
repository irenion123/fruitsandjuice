import json
import smtplib

from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db.models import Sum
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import TemplateView, RedirectView, ListView, View

from fruitsandjuice.forms import UserCreationForm
from fruitsandjuice.models import Product, Order, StatusChoice, OrderItem, DeliveryMethodChoice, PaymentMethodChoice
from fruitsandjuice.tokens import account_activation_token

User = get_user_model()


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


class OrderSuccessfulView(TemplateView):
    template_name = 'fruitandjuice/order_success.html'


class ShippayView(TemplateView):
    template_name = 'fruitandjuice/shippay.html'


class ProfileView(TemplateView):
    template_name = 'fruitandjuice/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['orders'] = Order.objects.filter(user_name=user)
        return context


class RegistrationSucessView(TemplateView):
    template_name = 'fruitandjuice/success_registration.html'


class OrderView(View):

    def post(self, request, *args, **kwargs):
        print('request: ', request.POST)
        pk = kwargs['pk']
        order = Order.objects.get(pk=pk)
        order.mobile = request.POST.get('mobile', '')
        order.delivery_method = request.POST.get('delivery_method', '')
        order.payment_method = request.POST.get('payment_method', '')
        order.adress = request.POST.get('address', '')
        order.status = StatusChoice.ACP.name
        order.save()
        return redirect('fruitsandjuice:order_success', pk=order.pk)


class CartView(ListView):
    template_name = 'fruitandjuice/cart.html'
    model = Order
    context_object_name = 'carts'

    def get_queryset(self):
        return Order.objects.filter(status=StatusChoice.FM.name, user_name=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        id_carts = context['carts']
        if id_carts:
            pk_cart = id_carts[0]
            context['delivery'] = [e for e in DeliveryMethodChoice]
            context['payment'] = [e for e in PaymentMethodChoice]
            context['pk_kart'] = pk_cart
            context['cart_items'] = OrderItem.objects.filter(order=pk_cart)
            context['summ_items'] = OrderItem.objects.filter(order=pk_cart).aggregate(Sum('product__price'))
        return context


class AddCartView(View):
    def post(self, request, *args, **kwargs):
        print('request: ', request.POST.get('item', None))
        item = request.POST.get('item', None)
        if item:
            cart, created = Order.objects.get_or_create(user_name=request.user, status=StatusChoice.FM.name)
            try:
                product = Product.objects.get(pk=int(item))
            except Product.DoesNotExist:
                return HttpResponse(status=404)
            item = OrderItem(order=cart, product=product)
            item.save()
        return HttpResponse('ОК', status=201)


class RemoveCartItemView(View):
    def post(self, request, *args, **kwargs):
        print('request: ', request.POST.get('item', None))
        item = request.POST.get('item', None)
        if item:
            OrderItem.objects.filter(pk=int(item)).delete()
            return HttpResponse(status=204)
        return HttpResponse(status=404)


class RegistrationView(View):
    def post(self, request, *args, **kwargs):
        print('request: ', request.POST)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            from_email = settings.EMAIL_HOST_USER
            to = form.cleaned_data.get('email')
            subject = 'Hi'
            template_html = 'fruitandjuice/mail.html'
            template_txt = 'fruitandjuice/mail.txt'
            ctx = {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }

            content_html = render_to_string(template_html, ctx)
            content_txt = render_to_string(template_txt, ctx)
            try:
                msg = EmailMultiAlternatives(subject, content_txt, from_email, [to])
                msg.attach_alternative(content_html, 'text/html')
                msg.send()
            except smtplib.SMTPException as e:
                print('Error: ', e)
            user_serializer = json.dumps(dict(user=user.username, email=user.email))
            return HttpResponse(user_serializer, content_type="application/json")
        else:
            return HttpResponse(form.errors.as_json(), content_type="application/json",
                                status=409)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse('fruitsandjuice:success_registration'))
    else:
        return HttpResponse('Activation link is invalid!')


def login_view(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        # user = authenticate(request, user=username, email='woodogul@gmail.com', password=password)
        print('--', user)
        if user is not None:
            login(request, user)
        else:
            print('login err!!!')
            return HttpResponse('{"message": "Неверный логин или пароль"}'.encode('utf-8'),
                                content_type="application/json",
                                status=403)
    return HttpResponse(b'ok')


@login_required
def logout(request):
    django_logout(request)
    return HttpResponseRedirect(reverse('fruitsandjuice:home'))


class AddItemOrder(View):
    def post(self, request, *args, **kwargs):
        print('Add item > request: ', request.POST)
