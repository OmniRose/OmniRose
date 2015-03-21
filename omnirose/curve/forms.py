from django import forms
from django.forms.models import formset_factory, BaseModelFormSet
from django.forms.widgets import NumberInput

from .models import Reading

class ReadingForm(forms.Form):
    ships_head = forms.IntegerField(required=False, widget=NumberInput(attrs={'style': "width: 5em;"}))
    deviation  = forms.FloatField(required=False,   widget=NumberInput(attrs={'style': "width: 5em;"}))

ReadingFormSet = formset_factory(form=ReadingForm)
