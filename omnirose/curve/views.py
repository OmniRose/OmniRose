import stripe

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.base import TemplateView

from django.shortcuts import redirect, render_to_response
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.http import urlencode
from django.utils.text import slugify
from django.conf import settings
from django.http import HttpResponse, FileResponse, Http404


from .models import Curve, Reading
from .forms import ReadingForm, ReadingFormSet, EquationChoiceForm, StripeForm, RoseDownloadForm

from omnirose.templatetags.omnirose_tags import east_west

from outputs.models import Rose, Table


class CurvePermissionMixin(object):

    def dispatch(self, *args, **kwargs):

        curve = self.get_object()
        user = self.request.user

        # TODO - will need to add smarts about public curves here
        if curve.user != user:
            return redirect('login')

        return super(CurvePermissionMixin, self).dispatch(*args, **kwargs)


class MayDownloadRoseMixin(object):

    def dispatch(self, *args, **kwargs):

        curve = self.get_object()

        # Check that rose downloads have been paid for.
        if not curve.may_download_roses:
            return redirect('curve_rose_purchase', pk=curve.pk)

        return super(MayDownloadRoseMixin, self).dispatch(*args, **kwargs)


class CurveView(CurvePermissionMixin, DetailView):

    model = Curve


class CurveVisualisationBaseView(CurvePermissionMixin, DetailView):
    model = Curve
    output = 'png'

    def get_visualisation_args(self):
        return {}

    def alter_curve(self, curve):
        pass

    @property
    def downloaded_name(self):
        curve = self.get_object()
        return slugify(curve.vessel) + "-table.pdf"


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

            response['Content-Disposition'] = "attachment; filename='" + self.downloaded_name + "'"

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


class CurveRosePdfView(MayDownloadRoseMixin, CurveVisualisationBaseView):
    visualisation_class = Rose
    output='pdf'

    @property
    def downloaded_name(self):
        curve = self.get_object()

        var_min = east_west(int(self.kwargs['var_min']))
        var_max = east_west(int(self.kwargs['var_max']))

        name = "%s-roses-%s-%s" % (curve.vessel, var_min, var_max)
        return slugify(name) + ".pdf"

    def get_visualisation_args(self):
        var_min = int(self.kwargs['var_min'])
        var_max = int(self.kwargs['var_max'])

        if var_min < -179 or var_min > 180 or var_max < -179 or var_max > 180 or var_max < var_min:
            raise Http404("Bad arguments for variation.")

        return {'variation': var_min, 'variation_max': var_max}


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


from .regions import regions
class CurveRosesSelect(CurvePermissionMixin, MayDownloadRoseMixin, CurveSetObjectMixin, FormView):
    model = Curve
    template_name = "curve/roses_select.html"
    form_class = RoseDownloadForm

    def get_context_data(self, **kwargs):
        context = super(CurveRosesSelect, self).get_context_data(**kwargs)
        context['regions'] = regions
        return context

    def form_valid(self, form):
        curve = self.object
        var_min = form.cleaned_data['from_variation']
        var_max = form.cleaned_data['to_variation']

        # swap them over if are the wrong way round
        if var_min > var_max:
            var_min, var_max = var_max, var_min

        return redirect('curve_rose_pdf', pk=curve.id, var_min=var_min, var_max=var_max)


class CurveRosesPurchaseFailed(CurvePermissionMixin, CurveSetObjectMixin, TemplateView):
    model = Curve
    template_name = "curve/roses_purchase_failed.html"

    def get_context_data(self, **kwargs):
        context = super(CurveRosesPurchaseFailed, self).get_context_data(**kwargs)
        context['message'] = self.request.GET.get('message')
        return context


class CurveRosesPurchase(CurvePermissionMixin, CurveSetObjectMixin, FormView):
    model = Curve
    template_name = "curve/roses_purchase.html"
    form_class = StripeForm

    def get_context_data(self, **kwargs):
        context = super(CurveRosesPurchase, self).get_context_data(**kwargs)
        context['STRIPE_PUBLIC_KEY'] = settings.STRIPE_PUBLIC_KEY
        context['ROSE_CURRENCY'] = settings.ROSE_CURRENCY
        context['ROSE_PRICE']    = settings.ROSE_PRICE
        context['ROSE_FORMATTED_PRICE'] = settings.ROSE_FORMATTED_PRICE
        return context

    def form_valid(self, form):

        curve = self.object

        # print form.cleaned_data

        # Set your secret key: remember to change this to your live secret key in production
        # See your keys here https://dashboard.stripe.com/account/apikeys
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe_token = form.cleaned_data['stripeToken']

        # Create the charge on Stripe's servers - this will charge the user's card
        try:
            charge = stripe.Charge.create(
              source               = stripe_token,
              receipt_email        = self.request.user.email,
              statement_descriptor = "conversion rose " + str(curve.id),
              amount               = settings.ROSE_PRICE,
              currency             = settings.ROSE_CURRENCY,
              description          = "Conversion roses for " + curve.vessel,
            )
            curve.set_roses_paid_to_now()
            curve.save()
            return redirect('curve_rose_select', pk=curve.id)

        except stripe.error.CardError, e:
            # There has been some error, tell the user.
            body = e.json_body
            err  = body['error']
            message =  err['message']

            failure_url = reverse('curve_rose_purchase_failed', kwargs={'pk':curve.id})
            failure_url = failure_url + '?' + urlencode({'message':message})

            return redirect(failure_url)
