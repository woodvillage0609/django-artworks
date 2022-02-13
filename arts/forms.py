from django import forms
from .models import Arts


class ArtsForm(forms.ModelForm):

    class Meta:
        model = Arts
        fields =  ['image', 'action'] 
