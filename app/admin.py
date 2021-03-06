from django.contrib import admin

from .models import Product, Category, Review, Company, Speciality, Cart, CartProduct, Favorites, FavoriteProduct, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'image',
        'price',
        'brand',
        'description',
        'category',
        'availability',
    )
    list_filter = ('brand', 'category', 'availability')
    raw_id_fields = ('review',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'stars', 'text', 'product')
    list_filter = ('owner', 'product')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'logo', 'speciality')
    list_filter = ('owner', 'speciality')


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'final_quantity',
        'final_price',
        'anon',
        'in_order',
    )
    list_filter = ('owner', 'anon', 'in_order')
    raw_id_fields = ('products',)


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'qty', 'cart', 'final_price', 'user')
    list_filter = ('product', 'cart', 'user')


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner')
    list_filter = ('owner',)
    raw_id_fields = ('products',)


@admin.register(FavoriteProduct)
class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'owner')
    list_filter = ('product', 'owner')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'address',
        'phone',
        'email',
        'comment',
        'date_at',
        'published_at',
        'cart',
        'owner',
    )
    list_filter = ('date_at', 'published_at', 'cart', 'owner')
