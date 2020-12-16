from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from.models import Profile


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Username',
        max_length=30,
        help_text='username should not contain spaces',
        widget=forms.TextInput(
            attrs={
                "id": "username"
            }
        )
    )
    email = forms.EmailField(label='E-Mail')

    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput(), min_length=8)
    password2 = forms.CharField(
        label='Password Confirmation', widget=forms.PasswordInput(), min_length=8)
    balance = forms.FloatField()

    class Meta:
        model = User
        fields = ('username',
                  'email', 'password1', 'password2', 'balance')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError(
                'Password doesnt match password confirmation')
        return cd['password2']

    def clean_username(self):
        cd = self.cleaned_data
        if User.objects.filter(username=cd['username']).exists():
            raise forms.ValidationError(
                'Username is exist .. Please try another username')
        return cd['username']

class LoginForm(forms.ModelForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']
