from django import template

register = template.Library()

@register.filter
def star_rating(value):
    value = int(value or 0)
    return "★" * value + "☆" * (5 - value)
