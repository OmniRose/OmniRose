from django.conf.urls import url, include
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='swinging/home.html'), name='swinging_home'),
    url(r'^compass_theory/$', TemplateView.as_view(template_name='swinging/compass_theory.html'), name='swinging_compass_theory'),

    url(r'^sun/$', TemplateView.as_view(template_name='swinging/sun_home.html'), name='swinging_sun_home'),
]


