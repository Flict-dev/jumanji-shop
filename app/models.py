from django.contrib.auth import get_user_model
from django.db import models

from Shop.settings import PRODUCT_IMAGE_DIR, COMPANY_IMAGE_DIR

User = get_user_model()


class Product(models.Model):
    title = models.CharField(max_length=30, verbose_name='Название продукта')
    image = models.ImageField(upload_to=PRODUCT_IMAGE_DIR, verbose_name='Изображение')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    brand = models.ForeignKey('Company', on_delete=models.CASCADE, verbose_name='Бренд')
    description = models.TextField(max_length=1000, verbose_name='Описание', blank=True, null=True)
    review = models.ForeignKey('Review', on_delete=models.CASCADE, verbose_name='Отзыв', blank=True, null=True,
                               related_name='product_review')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    availability = models.BooleanField(default=True, verbose_name='Наличие', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Category(models.Model):
    title = models.CharField(max_length=30, verbose_name='Название категории')


class Review(models.Model):
    RATING_CHOICES = [
        ('FN', '★★★★★'),
        ('GD', '★★★★'),
        ('BD', '★★★'),
        ('VB', '★★'),
        ('AL', '★'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.CharField(choices=RATING_CHOICES, default='AL', max_length=20)
    text = models.TextField(max_length=500, verbose_name='Озыв')
    product = models.ForeignKey('Product', verbose_name='Продукт', on_delete=models.CASCADE,
                                related_name='review_product')


class Company(models.Model):
    title = models.CharField(max_length=30, verbose_name='Название компании')
    owner = models.OneToOneField(User, verbose_name='Владелец', on_delete=models.CASCADE)
    logo = models.ImageField(upload_to=COMPANY_IMAGE_DIR, verbose_name='Лого')
    speciality = models.ForeignKey('Speciality', on_delete=models.CASCADE, verbose_name='Специализация')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Speciality(models.Model):
    title = models.CharField(max_length=30, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'


class Cart(models.Model):
    products = models.ManyToManyField('CartProduct', verbose_name='Продукты', blank=True, related_name='products')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец', blank=True)
    final_quantity = models.PositiveIntegerField(verbose_name='Кол-во товара', default=0, null=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Окончательная цена', default=0,
                                      null=True)
    anon = models.BooleanField(default=False, verbose_name='Анон')

    def __str__(self):
        return f'Корзина пользователья - {self.owner.username}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartProduct(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт')
    qty = models.PositiveIntegerField(default=1, verbose_name='Кол-во товара')
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, verbose_name='Корзина')
    final_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Окончательная цена продукта')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец', null=True)  # Убрать null

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super(CartProduct, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Продукт для корзины'
        verbose_name_plural = 'Продукты для корзины'

    def __str__(self):
        return f'Продукт для корзины пользователя - {self.cart.owner.username}'
