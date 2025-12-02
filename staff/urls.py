from django.urls import path

from .views import *

urlpatterns = [
    path('dashboard/', StaffHomeView.as_view(), name='staff_home'),
]
