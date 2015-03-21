from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^new/', views.CurveCreateView.as_view(),   name='curve_create'),
    url(r'^yours/', views.YourCurveListView.as_view(), name='curve_list'),
    url(r'^(?P<pk>\d)/$', views.CurveView.as_view(), name='curve_detail'),
    url(r'^(?P<pk>\d)/readings/$', views.CurveReadingEditView.as_view(), name='curve_readings'),
]

