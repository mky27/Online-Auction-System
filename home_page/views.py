from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, PersonalInfoForm, LoginForm
from .models import OASuser

# Create your views here.

def home_page(request):
    context = {}
    context['title'] = "Main Page | Bidify"
    return render(request, 'home_page.html', context)
  
def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            userPass = form.cleaned_data['userPass']
            user = authenticate(request, username=username, userPass=userPass)
            if user is not None:
                login(request, user)
                # Redirect to a success page
                return redirect('home_page')
            else:
                # Invalid login
                context = {'form': form, 'error' : "Invalid username or password.", 'title': "Login | Bidify"}
    else:
        form = LoginForm()
        context = {'form': form, 'title': "Login | Bidify"}
    return render(request, 'login.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            userPass = form.cleaned_data['userPass']
            confirm_password = form.cleaned_data['confirm_password']
            if userPass != confirm_password:
                context = {'form': form, 'error': 'Passwords do not match.', 'title': 'Register | Bidify'}
            else:
                try:
                    OASuser.objects.create(username=username, userPass=make_password(userPass)) # Save user registration data to OASuser table
                    return redirect('register_pi', username=username) # Redirect to register_pi view with user's username as a parameter
                except IntegrityError:
                    context = {'form': form, 'error': 'Username already exists. Please choose a different username.', 'title': 'Register | Bidify'}
    else:
        form = UserRegistrationForm()
        context = {'title': "Register | Bidify", 'form': form}
    return render(request, 'register.html', context)

def register_pi(request, username):
    user = OASuser.objects.get(username=username)
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST)
        if form.is_valid():
            fName = form.cleaned_data['fName']
            lName = form.cleaned_data['lName']
            date_of_birth = form.cleaned_data['date_of_birth']
            gender = form.cleaned_data['gender']
            phoneNo = form.cleaned_data['phoneNo']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            user.fName = fName
            user.lName =lName
            user.date_of_birth = date_of_birth
            user.gender = gender
            user.phoneNo = phoneNo
            user.email = email
            user.address = address
            user.save() # Save personal information data to OASuser table
            return redirect('login')
    else:
        form = PersonalInfoForm()
        context = {'title': "Personal Info | Bidify", 'form': form, 'username': username}
        return render(request, 'register_pi.html', context)
