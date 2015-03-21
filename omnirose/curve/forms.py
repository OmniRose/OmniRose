from django import forms
from django.forms.models import modelformset_factory

from .models import Reading

class ReadingForm(forms.ModelForm):
    class Meta:
        model = Reading
        fields = ['ships_head', 'deviation']

# class BaseReadingFormSet(BaseModelFormSet):
#     def __init__(self, *args, **kwargs):
#         super(BaseAuthorFormSet, self).__init__(*args, **kwargs)
#         self.queryset = Author.objects.filter(name__startswith='O')

# ReadingFormSet = modelformset_factory(Reading, form=ReadingForm)
