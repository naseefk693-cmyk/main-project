from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import UserProfile

class RegistrationForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('donor', 'Donor'), ('ngo', 'NGO'), ('admin', 'Admin')]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=True)
    phone = forms.CharField(
        max_length=17, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+911234567890'}),
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if self.cleaned_data['role'] == 'admin':
            user.is_staff = True
            user.is_superuser = True
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                address=self.cleaned_data['address'],
                phone=self.cleaned_data['phone']
            )
        return user

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
