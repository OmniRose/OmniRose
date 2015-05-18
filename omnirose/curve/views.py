from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.detail import DetailView, SingleObjectMixin

from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.text import slugify

from django.http import HttpResponse, FileResponse, Http404


from .models import Curve, Reading
from .forms import ReadingForm, ReadingFormSet, EquationChoiceForm

from outputs.models import Rose, Table


class CurvePermissionMixin(object):

    def dispatch(self, *args, **kwargs):

        curve = self.get_object()
        user = self.request.user

        # TODO - will need to add smarts about public curves here
        if curve.user != user:
            return redirect('login')

        return super(CurvePermissionMixin, self).dispatch(*args, **kwargs)


class CurveView(CurvePermissionMixin, DetailView):

    # FIXME - add logic to check that user owns this curve or it is public

    model = Curve


class CurveVisualisationBaseView(CurvePermissionMixin, DetailView):
    model = Curve
    output = 'png'

    def get_visualisation_args(self):
        return {}

    def alter_curve(self, curve):
        pass

    def get(self, request, *args, **kwargs):
        curve = self.get_object()
        self.alter_curve(curve)

        # Check that the curve can be calculated, otherwise bail here
        if not curve.can_calculate_curve:
            raise Http404("Cannot calculate curve, too few points perhaps?")

        kwargs = self.get_visualisation_args()
        vis = self.visualisation_class(curve=curve, **kwargs)
        vis.draw()

        # Create a response and write the png data to it
        if self.output == 'png':
            response = HttpResponse(content_type='image/png')
            vis.surface.write_to_png(response)
            return response
        elif self.output == 'pdf':

            # Need to manually finish to force writing to disk
            vis.surface.finish()

            response = FileResponse(
                open(vis.filename, 'rb'),
                content_type='application/pdf'
            )

            downloaded_name = slugify(curve.vessel) + "-table.pdf"
            response['Content-Disposition'] = "attachment; filename='" + downloaded_name + "'"

            return response
        else:
            raise Exception("can't produce output '%s'" % self.output)


class CurveTablePngView(CurveVisualisationBaseView):
    visualisation_class = Table

    def get_visualisation_args(self):
        if self.request.GET.get('crop', None):
            return { 'crop': True }
        else:
            return {}

    def alter_curve(self, curve):
        equation_slug = self.request.GET.get('equation', None)
        if equation_slug:
            curve.equation_slug = equation_slug


class CurveTablePdfView(CurveVisualisationBaseView):
    visualisation_class = Table
    output = 'pdf'

class CurveRosePngView(CurveVisualisationBaseView):
    visualisation_class = Rose

    def get_visualisation_args(self):
        return {'variation': -7}


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


class CurveSetObjectMixin(SingleObjectMixin):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CurveSetObjectMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CurveSetObjectMixin, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return self.get_object().get_absolute_url()


class CurveEquationSelectView(CurvePermissionMixin, CurveSetObjectMixin, FormView):
    model = Curve
    template_name = "curve/equation_select.html"
    form_class = EquationChoiceForm

    def get_form_kwargs(self):
        kwargs = super(CurveEquationSelectView, self).get_form_kwargs()
        kwargs['equation_choices'] = self.object.suitable_equations_as_choices()
        kwargs['equation_initial'] = self.object.equation_slug
        return kwargs

    def form_valid(self, form):
        curve = self.object
        curve.equation_slug = form['equation'].value()
        curve.save()
        return super(CurveEquationSelectView, self).form_valid(form)


class CurveDetailEditView(CurvePermissionMixin, UpdateView):
    model = Curve
    template_name = "curve/details_edit.html"
    fields = ['vessel','note']


class CurveReadingEditView(CurvePermissionMixin, CurveSetObjectMixin, FormView):
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

    def get_success_url(self):
        curve = self.get_object()
        if curve.can_calculate_curve:
            return reverse('curve_equation', kwargs={'pk': self.get_object().id } )
        else:
            return super(CurveReadingEditView, self).get_success_url()

