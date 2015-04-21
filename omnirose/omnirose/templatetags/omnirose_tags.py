# coding=utf-8

from django import template
# from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
# @stringfilter
def east_west(degrees):
    if degrees < 0:
        direction = "W"
    elif degrees > 0:
        direction = "E"
    else:
        direction = ""

    return u"%g°%s" % (abs(float(degrees)), direction)
