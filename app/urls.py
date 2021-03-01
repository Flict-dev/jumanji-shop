from django.urls import path

from app.views import (
    MainView,
    DetailProductView,
    AddToCart,
    CartView,
    DeleteFromCart,
    CatalogListView,
    DetailCompanyView,
    CategoryDetailView,
)

urlpatterns = [
    path('', MainView.as_view(), name='home'),
    path('products/<int:pk>', DetailProductView.as_view(), name='detail_product'),
    path('add-to-cart/product/<int:pk>', AddToCart.as_view(), name='add'),
    path('delete/from/cart/<int:pk>', DeleteFromCart.as_view(), name='delete_from_cart'),
    path('catalog/', CatalogListView.as_view(), name='catalog'),
    path('comapny/<int:pk>/', DetailCompanyView.as_view(), name='detail_company'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='detail_category'),  # Изменить на slug
    path('cart/', CartView.as_view(), name='cart')
]
