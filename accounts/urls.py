from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('register/user/', UserRegisterView.as_view(), name='user_register'),
    path('register/staff/', StaffRegisterView.as_view(), name='staff_register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
