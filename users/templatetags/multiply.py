from django import template

register = template.Library()

total = 0

@register.simple_tag
def multiply(quantity, price):
    return quantity*price
