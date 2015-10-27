from django.conf.urls import url, include
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [

    url(r'^(?P<pk>\d+)/$', views.SunSwingView.as_view(), name='sun_swing_detail'),

    url(r'^yours/', views.YourSunSwingListView.as_view(), name='swing_list'),

    # url(r'demo/', TemplateView.as_view(template_name='swing/demo.html'), name='swing_demo'),

    url(r'sun/',  TemplateView.as_view(template_name='swing/sun.html'), name='sun_demo'),
    url(r'sun_json/', views.JsonPostView.as_view(), name="sun_json"),
]

