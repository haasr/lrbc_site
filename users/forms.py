from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name  = forms.CharField(max_length=30, required=True)
    email      = forms.EmailField(max_length=254, required=True)
    username   = forms.CharField(max_length=30, required=True)
    password   = forms.CharField(max_length=30, required=True,
        widget=forms.PasswordInput,validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password' )