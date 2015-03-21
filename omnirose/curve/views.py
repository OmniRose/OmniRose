from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Curve

class CurveView(DetailView):

    model = Curve


class YourCurveListView(ListView):

    model = Curve
    template_name = "curve/your_curve_list.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(YourCurveListView, self).dispatch(*args, **kwargs)

    """Only curves belonging to this user"""
    def get_queryset(self):
        return self.request.user.curve_set.all()

class CurveCreateView(CreateView):

    model = Curve

    fields = ['vessel','note']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CurveCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()

        self.object = obj

        return redirect( self.get_success_url() )
