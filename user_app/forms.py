from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('donor', 'Donor'), ('ngo', 'NGO')]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)    #88
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

# forms.py
from django import forms
from .models import VisitorMessage, Review

class VisitorMessageForm(forms.ModelForm):
    class Meta:
        model = VisitorMessage
        fields = ['name', 'email', 'message']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'rating', 'comment']
