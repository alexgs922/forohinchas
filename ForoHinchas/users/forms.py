# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

from users.models import Profile


class UserFrom(forms.ModelForm):
    username = forms.CharField(label="Nombre de Usuario")
    username.widget.attrs['class'] = u'form-control'
    username.widget.attrs['placeholder'] = u'Username'
    email = forms.EmailField()
    email.widget.attrs['class'] = u'form-control'
    email.widget.attrs['placeholder'] = u'Email'
    first_name = forms.CharField(label="Nombre")
    first_name.widget.attrs['class'] = u'form-control'
    first_name.widget.attrs['placeholder'] = u'Nombre'
    last_name = forms.CharField(label="Apellidos")
    last_name.widget.attrs['class'] = u'form-control'
    last_name.widget.attrs['placeholder'] = u'Apellidos'
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput())
    password.widget.attrs['class'] = u'form-control'
    password.widget.attrs['placeholder'] = u'Contraseña'

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['team',]


class LoginForm(forms.Form):

    usr = forms.CharField(label="Username")
    pwd = forms.CharField(label="Contraseña", widget=forms.PasswordInput())
    usr.widget.attrs['class'] = u'form-control'
    usr.widget.attrs['placeholder'] = u'Username'
    pwd.widget.attrs['class'] = u'form-control'
    pwd.widget.attrs['placeholder'] = u'Contraseña'