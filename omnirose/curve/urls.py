from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^new/', views.CurveCreateView.as_view(),   name='curve_create'),
    url(r'^yours/', views.YourCurveListView.as_view(), name='curve_list'),
    url(r'^(?P<pk>\d+)/$', views.CurveView.as_view(), name='curve_detail'),
    url(r'^(?P<pk>\d+)/table_png/$', views.CurveTableView.as_view(), name='curve_table_png'),
    url(r'^(?P<pk>\d+)/rose_png/$', views.CurveRoseView.as_view(), name='curve_rose_png'),
    url(r'^(?P<pk>\d+)/readings/$', views.CurveReadingEditView.as_view(), name='curve_readings'),
    url(r'^(?P<pk>\d+)/details/$', views.CurveDetailEditView.as_view(), name='curve_edit_details'),
    url(r'^(?P<pk>\d+)/equation/$', views.CurveEquationSelectView.as_view(), name='curve_equation'),
]

