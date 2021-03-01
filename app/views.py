from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.base import View

from app.forms import ReviewForm
from app.mixins import CartMixin
from app.models import Product, CartProduct, Cart, Review, Category, Company
from app.utils import recount_cart


class MainView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data()
        context['products'] = Product.objects.all()[:6]
        return context


class AddToCart(CartMixin, View):
    def get(self, request, *args, **kwargs):
        if self.cart.anon:
            messages.info(request, 'Зрегистрируйтесь для того чтобы добивить товар в корзину')
            return redirect('/login/')
        else:
            product = get_object_or_404(Product, pk=kwargs['pk'])
            try:
                product_for_cart = CartProduct.objects.get(product=product)
                product_for_cart.qty += 1
                product_for_cart.save()
            except ObjectDoesNotExist:
                product_for_cart = CartProduct.objects.create(
                    product=product,
                    cart=self.cart
                )
            self.cart.products.add(product_for_cart)
            recount_cart(self.cart)
            return redirect('/cart/')


class DeleteFromCart(CartMixin, View):
    def get(self, request, pk):
        cart_product = CartProduct.objects.get(pk=pk)
        cart_product.delete()
        recount_cart(self.cart)
        return redirect('/cart/')


@method_decorator(login_required, name='get')
class CartView(CartMixin, View):
    def get(self, request):
        cart = self.cart
        return render(request, 'main/cart.html', context={'cart': cart})


class DetailProductView(View):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        related_products = Product.objects.filter(
            Q(category__title__icontains=product.category.title)
        )
        form = ReviewForm
        reviews = Review.objects.filter(product=product)
        context = {
            'product': product,
            'related_products': related_products,
            'reviews': reviews,
            'form': form,
        }
        return render(request, 'main/detail_product.html', context=context)

    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        if form.is_valid():
            product = Product.objects.get(pk=kwargs['pk'])
            stars = form.cleaned_data['stars']
            text = form.cleaned_data['text']
            if request.user.is_authenticated:
                Review.objects.create(owner=request.user, text=text, stars=stars, product=product)
                messages.info(request, 'Спасибо за отзыв!')
                return redirect('/login/')
            else:
                messages.info(request, 'Для того, чтобы оставить отзыв вам необходимо зарегистрироваться')
                return redirect('/login/')
        return render(request, 'main/detail_product.html', context={'form': form})


class CatalogListView(TemplateView):
    template_name = 'main/catalog.html'

    def get_context_data(self, **kwargs):
        context = super(CatalogListView, self).get_context_data(**kwargs)
        context['companies'] = Company.objects.all()
        context['categories'] = Category.objects.all()
        return context


class DetailCompanyView(View):  # Продумать логику
    def get(self, request, *args, **kwargs):
        company = get_object_or_404(Company, pk=kwargs['pk'])
        products = Product.objects.filter(brand=company)
        context = {
            'products': products,
            'company': company,
        }
        return render(request, 'main/detail_company.html', context=context)


class CategoryDetailView(View):
    def get(self, request, *args, **kwargs):
        category = get_object_or_404(Category, pk=kwargs['pk'])
        categories = Category.objects.all().order_by('title')
        products = Product.objects.filter(category=category)
        context = {
            'category': category,
            'categories': categories,
            'products': products,
        }
        return render(request, 'main/detail_category.html', context=context)
