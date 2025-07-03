from django import template

register = template.Library()

@register.filter(name="filter_first")
def get_first_el(value):

    value = value.split(" ")
    result = value[0]

    return result
