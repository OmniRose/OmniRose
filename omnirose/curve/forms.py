from django import forms
from django.forms.models import formset_factory, BaseModelFormSet
from django.forms.widgets import NumberInput

from .models import Reading

class DegreeInput(NumberInput):

    """Set the default style"""
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        attrs['style'] = "width: 5em;"

        super(DegreeInput, self).__init__(attrs)

    """Strip decimal points if not needed"""
    def _format_value(self, value):
        return u"%g" % float(value)


class ReadingForm(forms.Form):
    ships_head = forms.FloatField(
        required=False,
        min_value=0,
        max_value=359,
        widget=DegreeInput(attrs={'tabindex': 0})
    )

    deviation = forms.FloatField(
        required=False,
        min_value=-180,
        max_value=180,
        widget=DegreeInput(attrs={'tabindex': 1})
    )

ReadingFormSet = formset_factory(form=ReadingForm)


class EquationChoiceForm(forms.Form):
    def __init__(self, equation_choices, equation_initial, *args, **kwargs):
        super(EquationChoiceForm, self).__init__(*args, **kwargs)

        self.fields['equation'] = forms.ChoiceField(choices=equation_choices, initial=equation_initial)


class StripeForm(forms.Form):
    stripeToken = forms.CharField()

class RoseDownloadForm(forms.Form):
    from_variation = forms.IntegerField(min_value=-179, max_value=180)
    to_variation   = forms.IntegerField(min_value=-179, max_value=180)
