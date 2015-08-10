from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib import admin

from .views import HomePageView

urlpatterns = patterns('',

    url(r'^$', HomePageView.as_view(), name='home'),

    url(r'about/', TemplateView.as_view(template_name='about.html'), name='about'),

    url(r'^accounts/', include('accounts.urls')),
    url(r'^curves/', include('curve.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
