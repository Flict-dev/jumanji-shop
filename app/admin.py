from django.contrib import admin

from .models import Product, Category, Review, Company, Speciality, Cart, CartProduct, Favorites


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'image',
        'price',
        'brand',
        'description',
        'review',
        'category',
        'availability',
    )
    list_filter = ('brand', 'review', 'category', 'availability')


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
    list_display = ('id', 'owner', 'final_quantity', 'final_price', 'anon')
    list_filter = ('owner', 'anon')
    raw_id_fields = ('products',)


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner')
    list_filter = ('owner',)
    raw_id_fields = ('products',)
