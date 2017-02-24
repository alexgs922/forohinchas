# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, logout as django_logout, login as django_login
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect
from django.views import View

from users.forms import LoginForm, UserFrom, ProfileForm
from users.models import Profile


class LoginView(View):

    def get(self, request):
        # form = LoginForm()
        error_messages = []
        form = LoginForm()
        context = {
            'errors': error_messages,
            'login_form': form
        }
        return render(request, 'users/login.html', context)

    def post(self, request):
        # form = LoginForm()
        error_messages = []
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('usr')
            password = form.cleaned_data.get('pwd')
            user = authenticate(username=username, password=password)
            if user is None:
                error_messages.append('Nombre de usuario o contraseña incorrectos')
            else:
                if user.is_active:
                    django_login(request, user)
                    url = request.GET.get('next', 'index') # si no existe parametro GET 'next', le mandamos a 'photos_home'
                    return redirect(url)
                else:
                    error_messages.append('El usuario no está activo')
        context = {
            'errors': error_messages,
            'login_form': form
        }
        return render(request, 'users/login.html', context)


class LogoutView(View):

    def get(self, request):
        if request.user.is_authenticated():
            django_logout(request)
        return redirect('index')


class RegistrationView(View):  # Vista de la Registracion basada en vistas de Django ( View )

    def get(self, request):
        form = UserFrom(prefix='user')
        form_profile = ProfileForm(prefix='profile')
        context = {
            'form': form,
            'form_profile': form_profile
        }
        return render(request, 'users/register.html', context)

    @transaction.atomic
    def post(self, request):
        form = UserFrom(request.POST, prefix='user')
        form_profile = ProfileForm(request.POST, prefix='profile')
        if form.is_valid() and form_profile.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            profile = form_profile.save(commit=False)
            profile.user = user
            profile.save()
            url = request.GET.get('next', 'index')
            return redirect(url)

        context = {
            'form': form,
            'form_profile': form_profile
        }
        return render(request, 'users/register.html', context)
