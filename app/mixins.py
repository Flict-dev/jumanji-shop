from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.views.generic.base import View

from app.models import Cart, Favorites


class CartMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(owner=request.user, in_order=False)
            except ObjectDoesNotExist:
                cart = Cart.objects.create(owner=request.user)
        else:
            cart = Cart.objects.create(anon=True)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)


class FavoritesMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                self.favorites = Favorites.objects.get(owner=request.user)
            except ObjectDoesNotExist:
                self.favorites = Favorites.objects.create(owner=request.user)
        else:
            messages.info(request, 'Вам необходимо зарегистрироваться, чтобы добовлять товары в избранное')
            return redirect('/login/')
        return super().dispatch(request, *args, **kwargs)
