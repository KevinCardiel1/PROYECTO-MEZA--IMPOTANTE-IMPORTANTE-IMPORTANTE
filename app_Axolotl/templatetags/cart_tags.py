from django import template
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

@register.simple_tag(takes_context=True)
def get_cart_count(context, user):
    try:
        if not user.is_authenticated:
            return 0
        perfil = user.usuario
        cart = getattr(perfil, 'cart', None)
        if cart is None:
            return 0
        return cart.items.count()
    except Exception:
        return 0
