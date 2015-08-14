from django import forms
from .models import User

class RegistrationForm(forms.ModelForm):

    next = forms.CharField(max_length=200, required=False)

    class Meta:
        model = User
        fields = ['email', 'next']
