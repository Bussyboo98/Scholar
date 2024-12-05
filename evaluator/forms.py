from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import *


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Username*:',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'})
    )
    first_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Firstname'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Lastname'}))
    email = forms.EmailField(
        label='Email*:',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Email',
            'help_text': 'Required. Provide a valid email address.'
        })
    )
    password1 = forms.CharField(
        label='Enter Password:',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
    )
    password2 = forms.CharField(
        label='Confirm Password:',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match!")
        return cleaned_data

    def clean_email(self):
        email_field = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email_field).exists():
            raise forms.ValidationError('Email already exists.')
        return email_field

    class Meta:
        model = User  
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']



class EssayUploadForm(forms.ModelForm):
    essay_text = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Paste your essay here..."}),
        required=False,
        label="Essay Text",
    )
    essay_file = forms.FileField(
        required=False,
        label="Upload Essay File (.txt)",
    )
    
    class Meta:
        model = Evaluation 
        fields = ['essay_text', 'essay_file']

    def clean(self):
        cleaned_data = super().clean()
        essay_text = cleaned_data.get("essay_text")
        essay_file = cleaned_data.get("essay_file")

       
        if not essay_text and not essay_file:
            raise forms.ValidationError("Please provide either an essay text or upload a file.")
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class') is None:
                field.widget.attrs['class'] = 'form-control'