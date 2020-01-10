from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile



class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class UserForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ('first_name', 'last_name',)

class ProfileForm(forms.ModelForm):
    contact = forms.CharField(required=True)
    class Meta:
        model = Profile
        fields = ('contact', 'branch', 'semester')
