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
        return u"%g" % value


class ReadingForm(forms.Form):
    ships_head = forms.FloatField(
        required=False,
        widget=DegreeInput()
    )

    deviation = forms.FloatField(
        required=False,
        widget=DegreeInput()
    )

ReadingFormSet = formset_factory(form=ReadingForm)
