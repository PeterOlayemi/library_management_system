from django.shortcuts import render, redirect
from django.views import generic, View
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView as AuthLoginView

# Create your views here.

class UserRegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/user_signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = False
        user.save()

        messages.info(self.request, 'Registration successful. You can log in now.')
        return redirect('login')

class StaffRegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/staff_signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = True
        user.save()

        messages.info(self.request, 'Registration successful. You can log in now.')
        return redirect('login')

class LoginView(AuthLoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_staff:
            return reverse_lazy('staff_home')
        return reverse_lazy('user_home')
    