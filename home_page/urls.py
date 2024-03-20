from django.urls import path
from . import views

urlpatterns = [
    path('home_page/', views.home_page, name='home_page'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('register_pi/', views.register_pi, name='register_pi'),
]