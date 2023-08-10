from django import forms
from .models import Uitspraak


class LabelForm(forms.ModelForm):
    class Meta:
        model = Uitspraak
        fields = ['label']