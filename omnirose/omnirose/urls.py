from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import HomePageView

urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomePageView.as_view(), name='home'),

    url(r'^accounts/', include('accounts.urls')),
    url(r'^curves/', include('curve.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
