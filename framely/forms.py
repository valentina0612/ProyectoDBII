from django import forms
from .models import Usuario
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UsuarioForm(UserCreationForm):
    first_name = forms.CharField(max_length=140, required=True, widget=forms.TextInput(attrs={'class': 'campoNombre'}))
    last_name = forms.CharField(max_length=140, required=False, widget=forms.TextInput(attrs={'class': 'campoApellido'}))
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class': 'campoEmail'}))
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'campoUsuario'}))
    password1 = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class': 'campoPassword1'}))
    password2 = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class': 'campoPassword2'}))

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'campoInicio'}))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'class': 'campoInicioContraseña'}))