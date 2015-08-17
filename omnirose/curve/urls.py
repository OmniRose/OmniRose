from django.conf.urls import url, include
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='curve/curve_home.html'), name='curve_home'),

    url(r'^new/', views.CurveCreateView.as_view(),   name='curve_create'),
    url(r'^yours/', views.YourCurveListView.as_view(), name='curve_list'),

    url(r'^(?P<pk>\d+)/$', views.CurveView.as_view(), name='curve_detail'),

    url(r'^(?P<pk>\d+)/table_png/$', views.CurveTablePngView.as_view(), name='curve_table_png'),
    url(r'^(?P<pk>\d+)/table_pdf/$', views.CurveTablePdfView.as_view(), name='curve_table_pdf'),

    url(r'^(?P<pk>\d+)/rose_png/$', views.CurveRosePngView.as_view(), name='curve_rose_png'),
    url(r'^(?P<pk>\d+)/rose_purchase/$', views.CurveRosesPurchase.as_view(), name='curve_rose_purchase'),
    url(r'^(?P<pk>\d+)/rose_select/$', views.CurveRosesSelect.as_view(), name='curve_rose_select'),

    url(r'^(?P<pk>\d+)/readings/$', views.CurveReadingEditView.as_view(), name='curve_readings'),
    url(r'^(?P<pk>\d+)/details/$', views.CurveDetailEditView.as_view(), name='curve_edit_details'),
    url(r'^(?P<pk>\d+)/equation/$', views.CurveEquationSelectView.as_view(), name='curve_equation'),
]

