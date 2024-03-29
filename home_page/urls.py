from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('login/', views.log_in, name='login'),
    path('register/', views.register, name='register'),
    path('register_pi/<str:username>/', views.register_pi, name='register_pi'),
]