from django import template
from EcommerceApp.models import Category

register = template.Library()

@register.filter

def catagory(user):
    if user.is_authenticated:
        cat = Category.objects.filter(parent = None)
        return cat