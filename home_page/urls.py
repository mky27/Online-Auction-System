from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('login/', views.log_in, name='login'),
    path('register/', views.register, name='register'),
    path('register_pi/<str:username>/', views.register_pi, name='register_pi'),
    path('logout/', views.log_out, name='logout'),
    path('forgot_pass/', views.forgot_pass, name='forgot_pass'),
    path('reset_pass/', views.reset_pass, name='reset_pass'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]