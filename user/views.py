from django.shortcuts import render
from django.views.generic import View, TemplateView
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from.models import *

class Register(View):
    form_class = RegisterForm
    template_name = 'user/register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_profile = Profile(user=new_user) 
            new_profile.balance = form.cleaned_data['balance']
            new_user.save()
            new_profile.save()

            return redirect('login')
        else:
            return render(request, self.template_name, {'form': form})


class Login(View):
    from_class = LoginForm
    template_name = 'user/login.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(
                request, 'There is error in username or password .. please try again')
        return render(request, 'user/login.html', {})


class Logout(View):
    template_name = 'user/logout.html'

    def get(self, request):
        logout(request)
        return render(request, 'user/logout.html')
