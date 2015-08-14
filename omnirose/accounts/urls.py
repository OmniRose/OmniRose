from django.conf.urls import url, include
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    url(r'^enter/$', TemplateView.as_view(template_name='accounts/enter.html'), name='enter'),
    url(r'^register/$', views.RegistrationView.as_view(), name='register'),
    url(r'^', include('django.contrib.auth.urls')),
]

