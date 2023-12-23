from django import forms

from .models import Preference


class PreferenceForm(forms.ModelForm):
    class Meta:
        model = Preference
        fields = ["ai_model", "sentence_count"]
