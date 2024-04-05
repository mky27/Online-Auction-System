from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from .forms import UserRegistrationForm, PersonalInfoForm, LoginForm, ForgotPassForm, ResetPassForm
from .models import OASuser

# Create your views here.

def home_page(request):
    context = {}
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
                context = {'form': form, 'error' : "Invalid username or password."}
    else:
        form = LoginForm()
        context = {'form': form}
    return render(request, 'login.html', context)


def log_out(request):
    logout(request)
    return redirect('home_page')  


def register(request):
    context = {}  
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            userPass = form.cleaned_data['userPass']
            confirm_password = form.cleaned_data['confirm_password']
            if userPass != confirm_password:
                context['form'] = form
                context['error'] = 'Passwords do not match.'
            else:
                try:
                    # Validate the password
                    validate_password(userPass)
                    # Save user registration data to OASuser table
                    OASuser.objects.create(username=username, userPass=make_password(userPass))
                    return redirect('register_pi', username=username)
                except ValidationError as e:
                    context['form'] = form
                    context['error'] = e.messages[0]
                except IntegrityError:
                    context['form'] = form
                    context['error'] = 'Username already exists. Please choose a different username.'
    else:
        form = UserRegistrationForm()
        context['form'] = form
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
        context = {'form': form, 'username': username}
    return render(request, 'register_pi.html', context)


def forgot_pass(request):
    if request.method == 'POST':
        form = ForgotPassForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            # Check if the username and email match
            try:
                user = OASuser.objects.get(username=username, email=email)
                request.session['reset_user_id'] = user.id  # Store user ID in session
                return redirect('reset_pass')
            except OASuser.DoesNotExist:
                error = "Username and email do not match"
                return render(request, 'forgot_pass.html', {'form': form, 'error': error})
    else:
        form = ForgotPassForm()
    return render(request, 'forgot_pass.html', {'form': form})


def reset_pass(request):
    context = {}
    if request.method == 'POST':
        form = ResetPassForm(request.POST)
        if form.is_valid():
            userPass = form.cleaned_data['userPass']
            confirm_password = form.cleaned_data['confirm_password']
            if userPass != confirm_password:
                context['form'] = form
                context['error'] = "Passwords do not match."
                return render(request, 'reset_pass.html', context)
            else:
                try:
                    # Validate the password
                    validate_password(userPass)
                    user_id = request.session.get('reset_user_id')
                    if user_id:
                        user = OASuser.objects.get(id=user_id)
                        user.set_password(userPass)
                        user.save()
                        del request.session['reset_user_id']
                        return redirect('login')  # Redirect to login page after password reset
                    else:
                        context['form'] = form
                        context['error'] = "User ID not found in session."
                        return render(request, 'forgot_pass.html', context)
                except ValidationError as e:
                    context['form'] = form
                    context['error'] = e.messages[0]
                except OASuser.DoesNotExist:
                    context['form'] = form
                    context['error'] = "User not found."
                    return render(request, 'forgot_pass.html', context)
    else:
        form = ResetPassForm()
        context['form'] = form
    return render(request, 'reset_pass.html', context)
