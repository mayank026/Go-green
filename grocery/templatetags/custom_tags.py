from django import template
from grocery.models import *
register = template.Library()


@register.simple_tag
def totalprice(pid, quantity):
    prod = Product.objects.get(id=pid)
    total = int(prod.price) * int(quantity)
    return total

@register.filter(name='grandtotal')
def grandtotal(data):
    cart = Cart.objects.filter(profile__user=data)
    total = 0
    for i in cart:
        total +=(int(i.product.price) * int(i.quantity))
    return total