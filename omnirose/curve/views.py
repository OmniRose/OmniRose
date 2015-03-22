from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView, SingleObjectMixin

from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Curve, Reading
from .forms import ReadingForm, ReadingFormSet

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

        return redirect( reverse('curve_readings', kwargs={'pk': obj.id}) )

class CurveReadingEditView(SingleObjectMixin, FormView):
    model = Curve
    template_name = "curve/readings_edit.html"

    def get_form_class(self):
        return ReadingFormSet

    def get_form_kwargs(self):
        kwargs = super(CurveReadingEditView, self).get_form_kwargs()

        if self.request.method == 'GET':

            # Get all the existing readings
            readings_dict = self.object.readings_as_dict

            # Add in every 15 degrees
            for angle in range(0, 360, 15):
                if angle not in readings_dict:
                    readings_dict[angle] = ''

            # Load up the formset with the inital values
            initial = []
            for ships_head, deviation in readings_dict.items():
                initial.append({'ships_head': ships_head, 'deviation': deviation})

            # Sort the entries
            def sort_key(x): return x['ships_head']
            initial = sorted(initial, key=sort_key)

            kwargs['initial'] = initial

        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CurveReadingEditView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CurveReadingEditView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(CurveReadingEditView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, formset):

        curve = self.object

        # Delete all the existing readings
        curve.reading_set.all().delete()

        for form in formset:
            ships_head = form['ships_head'].value()
            deviation  = form['deviation'].value()
            if ships_head == '' or deviation == '':
                continue
            curve.reading_set.create(ships_head=ships_head, deviation=deviation)

        return super(CurveReadingEditView, self).form_valid(form)