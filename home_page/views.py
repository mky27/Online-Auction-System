from django.shortcuts import loader, redirect, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def home_page(request):
  template = loader.get_template('home_page.html')
  return HttpResponse(template.render())
  
def login(request):
  template = loader.get_template('login.html')
  return HttpResponse(template.render()) 

def register(request):
  template = loader.get_template('register.html')
  return HttpResponse(template.render())

@csrf_exempt
def register_pi(request):
  template = loader.get_template('register_pi.html')
  return HttpResponse(template.render())