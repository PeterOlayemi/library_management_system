from django.urls import path

from .views import *

urlpatterns = [
    path('dashboard/', UserHomeView.as_view(), name='user_home'),
]
