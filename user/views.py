from django.shortcuts import render
from django.views.generic import TemplateView

from .mixins import UserRequiredMixin

# Create your views here.

class UserHomeView(UserRequiredMixin, TemplateView):
    template_name = 'user/home.html'
