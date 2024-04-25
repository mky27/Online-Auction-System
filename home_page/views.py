from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, PersonalInfoForm, LoginForm, ForgotPassForm, ResetPassForm, EditProfileForm, CreateAuctionForm, validate_username
from .models import OASuser, OASauction

# Create your views here.

def home_page(request):
    auctions = OASauction.objects.all()
    return render(request, 'home_page.html', {'auctions': auctions})
  
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
                    validate_username(username)
                    validate_password(userPass)
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
                error = "Username and email do not match."
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
                        return redirect('login')
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


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user.fName = form.cleaned_data['fName']
            user.lName = form.cleaned_data['lName']
            user.date_of_birth = form.cleaned_data['date_of_birth']
            user.gender = form.cleaned_data['gender']
            user.phoneNo = form.cleaned_data['phoneNo']
            user.email = form.cleaned_data['email']
            user.address = form.cleaned_data['address']
            user.save()
            return redirect('home_page')
    else:
        # Populate the form with user's current data
        initial_data = {
            'fName': user.fName,
            'lName': user.lName,
            'date_of_birth': user.date_of_birth,
            'gender': user.gender,
            'phoneNo': user.phoneNo,
            'email': user.email,
            'address': user.address
        }
        form = EditProfileForm(initial=initial_data)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def create_auction(request):
    if request.method == 'POST':
        form = CreateAuctionForm(request.POST, request.FILES)
        if form.is_valid():
            seller = request.user
            item_name = form.cleaned_data['item_name']
            item_desc = form.cleaned_data['item_desc']
            item_cat = form.cleaned_data['item_cat']
            start_bid = form.cleaned_data['start_bid']
            auction_created_time = timezone.localtime(timezone.now())  
            auction_end_time = form.cleaned_data['auction_end_time']
            picture1 = form.cleaned_data['picture1']
            picture2 = form.cleaned_data['picture2']
            picture3 = form.cleaned_data['picture3']
            picture4 = form.cleaned_data['picture4']

            auction = OASauction(seller=seller, item_name=item_name, item_desc=item_desc, item_cat=item_cat,
                                 start_bid=start_bid, auction_created_time=auction_created_time, auction_end_time=auction_end_time,
                                 picture1=picture1, picture2=picture2, picture3=picture3, picture4=picture4)
            auction.save()
            return redirect('home_page')  
    else:
        form = CreateAuctionForm()
    return render(request, 'create_auction.html', {'form': form})
