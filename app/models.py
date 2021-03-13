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
    review = models.ManyToManyField('Review', verbose_name='Отзыв', blank=True,
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
    brand = models.ManyToManyField('Company', verbose_name='Компания')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Review(models.Model):
    RATING_CHOICES = [
        ('5', '★★★★★'),
        ('4', '★★★★'),
        ('3', '★★★'),
        ('2', '★★'),
        ('1', '★'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Изменить на ForIn.. и переделать логику с добалением
    stars = models.CharField(choices=RATING_CHOICES, default=1, max_length=20)
    text = models.TextField(max_length=500, verbose_name='Озыв')
    product = models.ForeignKey('Product', verbose_name='Продукт',
                                on_delete=models.CASCADE,
                                related_name='review_product'
                                )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв пользователя - {self.owner}'


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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец', null=True)
    final_quantity = models.PositiveIntegerField(verbose_name='Кол-во товара', default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Окончательная цена', default=0)
    anon = models.BooleanField(default=False, verbose_name='Анон')
    in_order = models.BooleanField(default=False, verbose_name='Статус корзины')

    # Оптимизировать Mixin и посмотреть nullы
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super(CartProduct, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Продукт для корзины'
        verbose_name_plural = 'Продукты для корзины'

    def __str__(self):
        return f'Продукт для корзины пользователя - {self.cart.owner}'


class Favorites(models.Model):
    products = models.ManyToManyField('FavoriteProduct', verbose_name='Избранные продукты')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return self.owner.username


class FavoriteProduct(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт для избранного')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')

    def __str__(self):
        return self.owner.username

    class Meta:
        verbose_name = 'Продукт для fav'
        verbose_name_plural = 'Продукты для fav'


class Order(models.Model):
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    address = models.CharField(max_length=70, verbose_name='Адрес')
    phone = models.CharField(max_length=30, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Почта')
    comment = models.TextField(max_length=1000, verbose_name='Комментраий')
    date_at = models.DateField(verbose_name='Число получения заказа')
    published_at = models.DateTimeField(auto_now_add=True)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, verbose_name='Корзина')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')

    def __str__(self):
        return f'Заказ пользователя - {self.owner.username}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
