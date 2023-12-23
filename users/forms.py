from django import forms

from .models import Preference


class PreferenceForm(forms.ModelForm):
    class Meta:
        model = Preference
        fields = ["model_choice", "sentence_length"]
