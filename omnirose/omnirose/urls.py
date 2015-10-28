from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib import admin

from .views import HomePageView

urlpatterns = patterns('',

    url(r'^$', HomePageView.as_view(), name='home'),

    url(r'about/', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'privacy/', TemplateView.as_view(template_name='privacy.html'), name='privacy'),

    url(r'^accounts/', include('accounts.urls')),
    url(r'^deviation_tables/', include('curve.urls')),
    url(r'^swinging/', include('swinging.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^errors/404/', TemplateView.as_view(template_name='404.html'), name="error_404"),
    url(r'^errors/500/', TemplateView.as_view(template_name='500.html'), name="error_500"),
)
