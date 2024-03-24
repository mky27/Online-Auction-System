from django.shortcuts import loader, redirect, render
from django.views.decorators.csrf import csrf_exempt
from .forms import UserRegistrationForm, PersonalInfoForm
from .models import OASuser

# Create your views here.

def home_page(request):
  context = {}
  context['title'] = "Main Page | Bidify"
  return render(request, 'home_page.html', context)
  
def login(request):
  context = {}
  context['title'] = "Login | Bidify"
  return render(request, 'login.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password != confirm_password:
                return render(request, 'register.html', {'form': form, 'error': 'Passwords do not match.'})
            else:
                # Save user registration data to OASuser table
                user = OASuser.objects.create(username=username, password=password,)
                # Redirect to register_pi view with user's username as a parameter
                return redirect('register_pi', username=username)
    else:
        form = UserRegistrationForm()
        context = {}
        context['title'] = "Register | Bidify"
        context['form'] = form
    return render(request, 'register.html', context)

def register_pi(request, username):
    user = OASuser.objects.get(username=username)
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST)
        if form.is_valid():
            # Save personal information data to OASuser table
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            date_of_birth = form.cleaned_data['date_of_birth']
            gender = form.cleaned_data['gender']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            user.first_name = first_name
            user.last_name = last_name
            user.date_of_birth = date_of_birth
            user.gender = gender
            user.phone_number = phone_number
            user.email = email
            user.address = address
            user.save()
            return redirect('login')
    else:
        form = PersonalInfoForm()
    return render(request, 'register_pi.html', {'form': form, 'username': username})
