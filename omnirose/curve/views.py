from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView, SingleObjectMixin

from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Curve
from .forms import ReadingForm

class CurveView(DetailView):

    # FIXME - add logic to check that user owns this curve or it is public

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


class CurveReadingEditView(SingleObjectMixin, FormView):
    model = Curve
    template_name = "curve/readings_edit.html"
    form_class = ReadingForm

    def get(self, request, *args, **kwargs):
        # if not request.user.is_authenticated():
        #     return HttpResponseForbidden()
        self.object = self.get_object()
        return super(CurveReadingEditView, self).get(request, *args, **kwargs)


    def get_success_url(self):
        return self.get_object().get_absolute_url()

    # def get_context_data(self, **kwargs):
    #     context = super(CurveReadingEditView, self).get_context_data(**kwargs)
    #     context['form'] = AuthorInterestForm()
    #     return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print "Form Valid"
        reading = form.save(commit=False)
        reading.curve = self.get_object()
        reading.save()
        return super(CurveReadingEditView, self).form_valid(form)
