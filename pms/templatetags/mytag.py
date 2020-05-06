from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name="class")
def class_name(value):
    return value.__class__.__name__

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

@register.filter(name='group_name')
def group_name(user, group):
    grp = Group.objects.get(name=group)
    return grp

@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg