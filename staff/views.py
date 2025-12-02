from django.shortcuts import render
from django.views.generic import TemplateView

from .mixins import StaffRequiredMixin

# Create your views here.

class StaffHomeView(StaffRequiredMixin, TemplateView):
    template_name = 'staff/home.html'
