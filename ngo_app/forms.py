# forms.py
from django import forms
from .models import NGOMedia

class NGOMediaForm(forms.ModelForm):
    class Meta:
        model = NGOMedia
        fields = ['title', 'description', 'image', 'video']
