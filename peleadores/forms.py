from django import forms
from .models import Peleador

class PeleadorForm(forms.ModelForm):
    class Meta:
        model = Peleador
        fields = "__all__"
