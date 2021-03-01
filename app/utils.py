from django.db import models


def recount_cart(cart):
    cart_data = cart.products.aggregate(models.Sum('final_price'), models.Sum('qty'))
    cart.final_price = cart_data['final_price__sum']
    cart.final_quantity = cart_data['qty__sum']
    cart.save()
