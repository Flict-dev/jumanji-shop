from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Avg
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView
from django.views.generic.base import View

from app.forms import ReviewForm, OrderForm, ChangeQtyForm
from app.mixins import CartMixin, FavoritesMixin
from app.models import Product, CartProduct, Review, Category, Company, Favorites, FavoriteProduct, Order
from app.utils import recount_cart


def page404(request, exception):
    return render(request, 'errors/404.html')


class MainView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data()
        context['products'] = Product.objects.filter(availability=True)[:6]
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
                    cart=self.cart,
                    user=request.user,
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
        return render(request, 'main/cart.html', context={'cart': self.cart, 'form': ChangeQtyForm})


class ChangeQty(CartMixin, View):
    def post(self, request, **kwargs):
        product_cart = CartProduct.objects.get(user=request.user, pk=kwargs.get('pk'))
        form = ChangeQtyForm(request.POST)
        if form.is_valid():
            product_cart.qty = form.cleaned_data['number']
            product_cart.save()
            recount_cart(self.cart)
            return redirect('/cart/')
        return render(request, 'main/cart.html', context={'cart': self.cart, 'form': form})


# продумать момент с instance
class DetailProductView(View):
    def get(self, request, pk):
        user = request.user
        product = Product.objects.get(id=pk)
        related_products = Product.objects.filter(
            Q(category__title__icontains=product.category.title)
        )
        rate = product.review.aggregate(avg=Avg('stars'))['avg']
        try:
            form = ReviewForm(instance=product.review.get(owner=user))
        except ObjectDoesNotExist:
            form = ReviewForm
        context = {
            'product': product,
            'related_products': related_products.select_related('category'),
            'rate': rate,
            'form': form,
        }
        return render(request, 'main/detail_product.html', context=context)

    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        if form.is_valid():
            product = Product.objects.get(pk=kwargs['pk'])
            defaults = form.cleaned_data
            if request.user.is_authenticated:
                Review.objects.update_or_create(product=product, owner=request.user, defaults=defaults)
                new_rev = Review.objects.get(product=product)
                product.review.add(new_rev)
                product.save()
                messages.info(request, 'Спасибо за отзыв!')
                return redirect('/')
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
        categories = Category.objects.filter(brand=company)
        context = {
            'categories': categories,
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


class AddToFavorites(FavoritesMixin, View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['pk'])
        try:
            fav_product = FavoriteProduct.objects.get(product=product)
        except ObjectDoesNotExist:
            fav_product = FavoriteProduct.objects.create(owner=request.user, product=product)
        self.favorites.products.add(fav_product)
        self.favorites.save()
        return redirect('/favorites/')


class DelFromFavorites(FavoritesMixin, View):
    def get(self, request, **kwargs):
        try:
            favorite = self.favorites.products.get(pk=kwargs['pk'])
            favorite.delete()
            return redirect('/favorites/')
        except ObjectDoesNotExist:
            raise Http404


class FavoritesView(FavoritesMixin, ListView):
    template_name = 'main/favorites.html'
    model = Favorites
    paginate_by = 3

    def get_queryset(self):
        return FavoriteProduct.objects.filter(owner=self.request.user).select_related('product')


class MakeOrderView(CartMixin, View):
    def get(self, request):
        return render(request, 'main/order.html', context={'form': OrderForm, 'cart': self.cart})

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        if form.is_valid():
            self.cart.in_order = True
            self.cart.save()
            defaults = form.cleaned_data
            Order.objects.create(
                defaults=defaults,
                owner=request.user,
                cart=self.cart
            )
            messages.info(request, 'Спасибо за заказ!')
            return redirect('/')
        return render(request, 'main/order.html', context={'form': form, 'cart': self.cart})
# Сделать change_qty в Cart
# Сделать нормальный профиль с заказами
# Досмотреть ролик про пагинацию, админку
