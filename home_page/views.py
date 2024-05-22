from datetime import timedelta
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserRegistrationForm, PersonalInfoForm, LoginForm, ForgotPassForm, ResetPassForm, EditProfileForm, CreateAuctionForm, PlaceBidForm, EditAuctionForm, ChangePasswordForm, CheckoutForm, ReceiveForm, ReportForm, validate_username
from .models import OASuser, OASauction, OASwatchlist, OASauctionWinner, OAStransaction, OASreport
from decimal import Decimal


def home_page(request):
    manual_update_auction()

    query = request.GET.get('q', '')
    selected_category = request.GET.get('category', '')

    active_auctions = OASauction.objects.filter(
        is_ongoing=True, 
        auction_end_time__gt=timezone.now()
    )

    if query:
        active_auctions = active_auctions.filter(item_name__icontains=query)
    
    if selected_category:
        active_auctions = active_auctions.filter(item_cat=selected_category)

    context = {
        'active_auctions': active_auctions,
        'query': query,
        'selected_category': selected_category,
        'categories': [
            'Apparel & Accessories', 'Animal & Pet Supplies', 'Arts & Entertainment', 'Baby & Toddler',
            'Camera & Optics', 'Electronics', 'Food & Beverages', 'Furniture', 'Hardware', 
            'Home & Garden', 'Health & Beauty', 'Luggage & Bags', 'Office Supplies', 'Religious', 
            'Sporting Goods', 'Toys & Games', 'Vehicle & Parts', 'Others'
        ],
    }

    if request.user.is_authenticated and request.user.is_admin:
        return render(request, 'admin_home.html', context)
    
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
                if user.is_admin:
                    return redirect('admin_home')
                else:
                    return redirect('home_page')
            else:
                context = {'form': form, 'error' : "Invalid username or password."}
    else:
        form = LoginForm()
        context = {'form': form}
    return render(request, 'login.html', context)


@login_required
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
            user.save()
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
            try:
                user = OASuser.objects.get(username=username, email=email)
                request.session['reset_user_id'] = user.id
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
            action = request.POST.get('action')
            if action == 'save':
                seller = request.user
                item_name = form.cleaned_data['item_name']
                item_desc = form.cleaned_data['item_desc']
                item_cat = form.cleaned_data['item_cat']
                start_bid = form.cleaned_data['start_bid']
                auction_end_time = form.cleaned_data['auction_end_time']
                picture1 = form.cleaned_data['picture1']
                picture2 = form.cleaned_data['picture2']
                picture3 = form.cleaned_data['picture3']
                picture4 = form.cleaned_data['picture4']
                picture5 = form.cleaned_data['picture5']
                picture6 = form.cleaned_data['picture6']
                picture7 = form.cleaned_data['picture7']
                is_saved = True

                auction = OASauction(seller=seller, item_name=item_name, item_desc=item_desc, item_cat=item_cat,
                                    start_bid=start_bid, auction_end_time=auction_end_time, is_saved=is_saved,
                                    picture1=picture1, picture2=picture2, picture3=picture3, picture4=picture4,
                                    picture5=picture5, picture6=picture6, picture7=picture7,)
                auction.save()
                return redirect('home_page')
                
            elif action == 'post':
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
                picture5 = form.cleaned_data['picture5']
                picture6 = form.cleaned_data['picture6']
                picture7 = form.cleaned_data['picture7']
                is_ongoing = True

                auction = OASauction(seller=seller, item_name=item_name, item_desc=item_desc, item_cat=item_cat,
                                    start_bid=start_bid, auction_created_time=auction_created_time, auction_end_time=auction_end_time,
                                    picture1=picture1, picture2=picture2, picture3=picture3, picture4=picture4,
                                    picture5=picture5, picture6=picture6, picture7=picture7, is_ongoing=is_ongoing,)
                auction.save()
                return redirect('home_page')
    else:
        form = CreateAuctionForm()

    return render(request, 'create_auction.html', {'form': form})


@login_required
def auction_details(request, auction_id):
    auction = get_object_or_404(OASauction, pk=auction_id)
    time_left = auction.auction_end_time - timezone.now()
    seller_username = auction.seller.username
    in_watchlist = is_in_watchlist(request.user, auction)
    pictures = [
        auction.picture1.url if auction.picture1 else None,
        auction.picture2.url if auction.picture2 else None,
        auction.picture3.url if auction.picture3 else None,
        auction.picture4.url if auction.picture4 else None,
        auction.picture5.url if auction.picture5 else None,
        auction.picture6.url if auction.picture6 else None,
        auction.picture7.url if auction.picture7 else None,
    ]
    pictures = [pic for pic in pictures if pic] 

    context = {
        'auction': auction,
        'time_left': time_left,
        'seller_username': seller_username,
        'in_watchlist': in_watchlist,
        'pictures': pictures
    }
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'delete':
            #auction.delete()
            print("delete")
            return redirect('ongoing_auction') 
        
    return render(request, 'auction_details.html', context)


@login_required
def place_bid(request, auction_id):
    auction = get_object_or_404(OASauction, pk=auction_id)
    error_message = None
    success_message = None
    seller_username = auction.seller.username
    pictures = [
        auction.picture1.url if auction.picture1 else None,
        auction.picture2.url if auction.picture2 else None,
        auction.picture3.url if auction.picture3 else None,
        auction.picture4.url if auction.picture4 else None,
        auction.picture5.url if auction.picture5 else None,
        auction.picture6.url if auction.picture6 else None,
        auction.picture7.url if auction.picture7 else None,
    ]
    pictures = [pic for pic in pictures if pic] 

    if auction.auction_end_time <= timezone.now():
        error_message = "Sorry, the auction has ended. You can no longer place a bid on this item."
        return render(request, 'auction_details.html', {'auction': auction, 'error_message': error_message, 
                                                        'seller_username': seller_username, 'pictures': pictures})
    
    if request.user == auction.seller:
        error_message = "You cannot place a bid on your own item."
        return render(request, 'auction_details.html', {'auction': auction, 'error_message': error_message, 
                                                        'seller_username': seller_username, 'pictures': pictures})
    
    if request.method == 'POST':
        form = PlaceBidForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data['bid_amount']
            bid_increase = Decimal('0.1')
            if bid_amount >= auction.current_bid + bid_increase:  
                auction.second_highest_bid = auction.current_bid
                auction.second_highest_bidder = auction.current_bidder
                auction.current_bid = bid_amount
                auction.current_bidder = request.user
                auction.save()
                success_message = 'Your bid has been placed successfully.'
            else:
                error_message = 'Your bid must be at least 0.10 higher than the current bid.'
    else:
        form = PlaceBidForm()
    
    return render(request, 'auction_details.html', {'form': form, 'auction': auction, 'error_message': error_message, 
                                                    'success_message': success_message, 'seller_username': seller_username,
                                                    'pictures': pictures})


def auto_update_auction(request):
    auctions_to_update = OASauction.objects.filter(auction_end_time__lte=timezone.now(), is_ongoing=True)
    for auction in auctions_to_update:
        auction.is_ongoing = False
        auction.is_completed = True
        auction.save()

        highest_bid = auction.current_bid
        highest_bidder = auction.current_bidder
        OASauctionWinner.objects.create(
            auction=auction,
            winner=highest_bidder,
            winning_bid=highest_bid,
            checkout_deadline=timezone.now() + timedelta(days=7)
        )

        OASwatchlist.objects.filter(auction=auction).delete()

    return HttpResponse()


def manual_update_auction():
    auctions_to_update = OASauction.objects.filter(auction_end_time__lte=timezone.now(), is_ongoing=True)
    for auction in auctions_to_update:
        auction.is_ongoing = False
        auction.is_completed = True
        auction.save()

        highest_bid = auction.current_bid
        highest_bidder = auction.current_bidder
        OASauctionWinner.objects.create(
            auction=auction,
            winner=highest_bidder,
            winning_bid=highest_bid,
            checkout_deadline=timezone.now() + timedelta(days=7)
        )

        OASwatchlist.objects.filter(auction=auction).delete()


@login_required
def watchlist(request):
    watchlist_items = OASwatchlist.objects.filter(user=request.user)
    return render(request, 'watchlist.html', {'watchlist_items': watchlist_items})


@login_required
def add_to_watchlist(request, auction_id):
    auction = get_object_or_404(OASauction, pk=auction_id)
    user = request.user

    OASwatchlist.objects.create(user=user, auction=auction)

    return redirect('auction_details', auction_id=auction_id)


@login_required
def remove_from_watchlist(request, auction_id):
    auction = get_object_or_404(OASauction, pk=auction_id)
    user = request.user

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'remove_watchlist':
            OASwatchlist.objects.filter(user=user, auction=auction).delete()
            return redirect('watchlist')
        else:
            OASwatchlist.objects.filter(user=user, auction=auction).delete()
            return redirect('auction_details', auction_id=auction_id)


def is_in_watchlist(user, auction):
    return OASwatchlist.objects.filter(user=user, auction=auction).exists()


@login_required
def withdraw_from_auction(request, auction_id):
    auction = get_object_or_404(OASauction, pk=auction_id)

    if request.method == 'POST':
        if auction.second_highest_bid is not None and auction.second_highest_bidder is not None:
            auction.current_bid = auction.second_highest_bid
            auction.current_bidder = auction.second_highest_bidder
            auction.second_highest_bid = None
            auction.second_highest_bidder = None
        else:
            auction.current_bid = auction.start_bid
            auction.current_bidder = None
        auction.save()

        messages.success(request, 'You have successfully withdrawn from the auction.')
        
        return redirect('home_page') 
    
    return redirect('auction_details', auction_id=auction_id)


@login_required
def saved_auction(request):
    saved_auctions = OASauction.objects.filter(seller=request.user, is_saved=True)
    return render(request, 'saved_auction.html', {'saved_auctions': saved_auctions})


@login_required
def edit_auction(request, auction_id):
    auction = get_object_or_404(OASauction, pk=auction_id)

    if request.method == 'POST':
        form = EditAuctionForm(request.POST, request.FILES)
        if form.is_valid():
            action = request.POST.get('action')
            if action == 'save':
                auction.item_name = form.cleaned_data['item_name']
                auction.item_desc = form.cleaned_data['item_desc']
                auction.item_cat = form.cleaned_data['item_cat']
                auction.start_bid = form.cleaned_data['start_bid']
                auction.auction_end_time = form.cleaned_data['auction_end_time']
                auction.is_saved = True

                if 'picture1' in request.FILES:
                    auction.picture1 = request.FILES['picture1']
                if 'picture2' in request.FILES:
                    auction.picture2 = request.FILES['picture2']
                if 'picture3' in request.FILES:
                    auction.picture3 = request.FILES['picture3']
                if 'picture4' in request.FILES:
                    auction.picture4 = request.FILES['picture4']
                if 'picture5' in request.FILES:
                    auction.picture5 = request.FILES['picture5']
                if 'picture6' in request.FILES:
                    auction.picture6 = request.FILES['picture6']
                if 'picture7' in request.FILES:
                    auction.picture7 = request.FILES['picture7']

                auction.save()

            elif action == 'post':
                auction.item_name = form.cleaned_data['item_name']
                auction.item_desc = form.cleaned_data['item_desc']
                auction.item_cat = form.cleaned_data['item_cat']
                auction.start_bid = form.cleaned_data['start_bid']
                auction.auction_created_time = timezone.localtime(timezone.now())
                auction.auction_end_time = form.cleaned_data['auction_end_time']
                auction.is_saved = False
                auction.is_ongoing = True

                if 'picture1' in request.FILES:
                    auction.picture1 = request.FILES['picture1']
                if 'picture2' in request.FILES:
                    auction.picture2 = request.FILES['picture2']
                if 'picture3' in request.FILES:
                    auction.picture3 = request.FILES['picture3']
                if 'picture4' in request.FILES:
                    auction.picture4 = request.FILES['picture4']
                if 'picture4' in request.FILES:
                    auction.picture4 = request.FILES['picture4']
                if 'picture5' in request.FILES:
                    auction.picture5 = request.FILES['picture5']
                if 'picture6' in request.FILES:
                    auction.picture6 = request.FILES['picture6']
                if 'picture7' in request.FILES:
                    auction.picture7 = request.FILES['picture7']

                auction.save()

            elif action == 'delete':
                auction.delete()  
                return redirect('saved_auction') 
            
            return redirect('saved_auction')
         
    else:
        form = EditAuctionForm(initial={
            'item_name': auction.item_name,
            'item_desc': auction.item_desc,
            'item_cat': auction.item_cat,
            'start_bid': auction.start_bid,
            'auction_end_time': auction.auction_end_time,
        })
        
    return render(request, 'edit_auction.html', {'form': form, 'auction': auction})


@login_required
def completed_auction(request):
    completed_auctions = OASauction.objects.filter(seller=request.user, is_completed=True)
    
    return render(request, 'completed_auction.html', {'completed_auctions': completed_auctions})


@login_required
def completed_auction_details(request, auction_id):
    auction = get_object_or_404(OASauction, pk=auction_id)
    auction_winner = get_object_or_404(OASauctionWinner, auction_id=auction_id)

    deadline_passed = auction_winner.checkout_deadline < timezone.now()

    if request.method == 'POST':
        auction.delete()
        return redirect('completed_auction')
    
    return render(request, 'completed_auction_details.html', {'auction': auction, 'deadline_passed': deadline_passed, 'auction_winner': auction_winner})


@login_required
def ongoing_auction(request):
    ongoing_auctions = OASauction.objects.filter(seller=request.user, is_ongoing=True)
    return render(request, 'ongoing_auction.html', {'ongoing_auctions': ongoing_auctions})


@login_required
def change_pass(request):
    context = {}
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            user = request.user

            if not user.check_password(current_password):
                context['form'] = form
                context['error'] = "Current password is invalid."
                return render(request, 'change_pass.html', context)
            
            if current_password == new_password:
                context['form'] = form
                context['error'] = "New password must be different from current password."
                return render(request, 'change_pass.html', context)
            
            if new_password != confirm_password:
                context['form'] = form
                context['error'] = "New password and confirm password do not match."
                return render(request, 'change_pass.html', context)
            
            try:
                validate_password(new_password)
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password changed successfully.')
                return redirect('home_page')
            except ValidationError as e:
                context['form'] = form
                context['error'] = e.messages[0]
                return render(request, 'change_pass.html', context)
    else:
        form = ChangePasswordForm()
    return render(request, 'change_pass.html', {'form': form})


@login_required
def cart(request):
    won_auctions = OASauctionWinner.objects.filter(winner=request.user, is_checkout=False)

    return render(request, 'cart.html', {'won_auctions': won_auctions})


@login_required
def cart_auction_details(request, auction_id):
    auction_winner = get_object_or_404(OASauctionWinner, auction_id=auction_id)
    deadline_passed = auction_winner.checkout_deadline < timezone.now()
    pictures = [
        auction_winner.auction.picture1.url if auction_winner.auction.picture1 else None,
        auction_winner.auction.picture2.url if auction_winner.auction.picture2 else None,
        auction_winner.auction.picture3.url if auction_winner.auction.picture3 else None,
        auction_winner.auction.picture4.url if auction_winner.auction.picture4 else None,
        auction_winner.auction.picture5.url if auction_winner.auction.picture5 else None,
        auction_winner.auction.picture6.url if auction_winner.auction.picture6 else None,
        auction_winner.auction.picture7.url if auction_winner.auction.picture7 else None,
    ]
    pictures = [pic for pic in pictures if pic] 
    
    return render(request, 'cart_auction_details.html', {'auction_winner': auction_winner, 'deadline_passed': deadline_passed, 'pictures': pictures})


@login_required
def checkout(request, auction_winner_id):
    auction_winner = get_object_or_404(OASauctionWinner, id=auction_winner_id)
    buyer = auction_winner.winner
    pictures = [
        auction_winner.auction.picture1.url if auction_winner.auction.picture1 else None,
        auction_winner.auction.picture2.url if auction_winner.auction.picture2 else None,
        auction_winner.auction.picture3.url if auction_winner.auction.picture3 else None,
        auction_winner.auction.picture4.url if auction_winner.auction.picture4 else None,
        auction_winner.auction.picture5.url if auction_winner.auction.picture5 else None,
        auction_winner.auction.picture6.url if auction_winner.auction.picture6 else None,
        auction_winner.auction.picture7.url if auction_winner.auction.picture7 else None,
    ]
    pictures = [pic for pic in pictures if pic] 

    deadline_passed = auction_winner.checkout_deadline < timezone.now()
    
    if deadline_passed:
        return redirect('cart')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            auction_winner_id = request.POST.get('auction_winner_id')
            winning_bid = auction_winner.winning_bid
            winning_bid_decimal = Decimal(winning_bid)
            
            if request.user.balance < winning_bid_decimal:
                error = "Wallet balance insufficient."
                return render(request, 'checkout.html', {'auction_winner': auction_winner, 'form': form, 'error': error, 'pictures': pictures})
            
            request.user.balance -= winning_bid_decimal
            request.user.save()

            OAStransaction.objects.create(
                main_user=request.user,
                second_user=auction_winner.auction.seller,
                transaction_type='PAYMENT',
                amount=winning_bid_decimal,
                timestamp=timezone.now()
            )
            
            auction_winner.buyer_name = form.cleaned_data['buyer_name']
            auction_winner.buyer_phone = form.cleaned_data['buyer_phone']
            auction_winner.buyer_address = form.cleaned_data['buyer_address']
            auction_winner.is_checkout = True
            auction_winner.save()
            return redirect('home_page')
    else:
        initial_data = {
            'buyer_name': f"{buyer.fName} {buyer.lName}",
            'buyer_phone': buyer.phoneNo,
            'buyer_address': buyer.address,
        }
        form = CheckoutForm(initial=initial_data)

    return render(request, 'checkout.html', {'auction_winner': auction_winner, 'form': form, 'pictures': pictures})


def remove_from_cart(request, auction_winner_id):
    auction_winner = get_object_or_404(OASauctionWinner, id=auction_winner_id)
    auction_winner.delete()

    return redirect('cart')


@login_required
def get_wallet_balance(request):
    user_balance = request.user.balance
    
    return JsonResponse({'balance': user_balance})


@login_required
def wallet(request):
    transactions = OAStransaction.objects.filter(main_user=request.user).order_by('-timestamp')
    
    return render(request, 'wallet.html', {'transactions': transactions})


@login_required
def reload_wallet(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            amount = Decimal(amount)
            request.user.balance += amount
            request.user.save()

            OAStransaction.objects.create(
                main_user=request.user,
                second_user=request.user,  
                transaction_type='RELOAD',
                amount=amount,
                timestamp=timezone.now()
            )

            return redirect('wallet')
        except ValueError:
            pass  
    return redirect('wallet')


@login_required
def to_deliver(request):
    seller = request.user
    items_to_deliver = OASauctionWinner.objects.filter(auction__seller=seller, is_delivered=False)

    for auction_winner in items_to_deliver:
        auction_winner.deadline_passed = auction_winner.checkout_deadline < timezone.now()

    return render(request, 'to_deliver.html', {'items_to_deliver': items_to_deliver})


@login_required
def deliver_auction_detail(request, auction_winner_id):
    auction_winner = get_object_or_404(OASauctionWinner, id=auction_winner_id)

    if request.method == 'POST':
        if 'out_for_delivery' in request.POST:
            auction_winner.is_delivered = True
            auction_winner.save()
            return redirect('to_deliver')
        elif 'remove' in request.POST:
            auction_winner.delete()
            return redirect('to_deliver')

    deadline_passed = auction_winner.checkout_deadline < timezone.now()

    return render(request, 'deliver_auction_details.html', {
        'auction_winner': auction_winner,
        'deadline_passed': deadline_passed
    })


@login_required
def to_receive(request):
    user = request.user
    items_to_receive = OASauctionWinner.objects.filter(winner=user, is_checkout=True, is_received=False)
    return render(request, 'to_receive.html', {'items_to_receive': items_to_receive})


@login_required
def receive_auction_details(request, auction_winner_id):
    auction_winner = get_object_or_404(OASauctionWinner, id=auction_winner_id)
    auction = get_object_or_404(OASauction, pk=auction_winner.auction_id)

    if request.method == 'POST':
        form = ReceiveForm(request.POST)
        if form.is_valid():
            auction.comment = form.cleaned_data['comment']
            auction.ratings = form.cleaned_data['ratings']
            auction_winner.is_received = True
            auction.save()
            auction_winner.save()
            return redirect('to_receive')
    else:
        form = ReceiveForm()

    return render(request, 'receive_auction_details.html', {'auction_winner': auction_winner, 'form': form})


@login_required
def report(request):
    user = request.user

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            OASreport.objects.create(
                user = request.user,
                category = form.cleaned_data['category'],
                title = form.cleaned_data['title'],
                content = form.cleaned_data['content'],
                created_at = timezone.now()
            )
            return redirect('home_page')
    else:
        form = ReportForm()
    return render(request, 'report.html', {'form': form, 'user': user})


def view_profile(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('login')
    
    ongoing_auctions = OASauction.objects.filter(seller=user, is_ongoing=True)
    completed_auctions = OASauction.objects.filter(seller=user, is_completed=True)

    context = {
        'user': user,
        'ongoing_auctions': ongoing_auctions,
        'completed_auctions': completed_auctions
    }
    return render(request, 'view_profile.html', context)


@user_passes_test(lambda u: u.is_admin)
def manage_user(request):
    query = request.GET.get('q', '')

    users = OASuser.objects.filter(is_admin=False)

    if query:
        users = users.filter(username__icontains=query)

    context = {
        'users': users,
        'query': query,
    }
    return render(request, 'manage_user.html', context)


@user_passes_test(lambda u: u.is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(OASuser, id=user_id)
    
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('manage_user')


@user_passes_test(lambda u: u.is_admin)
def view_user_profile(request, user_id):
    user = get_object_or_404(OASuser, id=user_id)
    context = {'user': user}
    return render(request, 'view_user_profile.html', context)


@user_passes_test(lambda u: u.is_admin)
def manage_trans(request):
    transactions = OAStransaction.objects.filter(transaction_type='PAYMENT', approved=False, rejected=False)

    context = {
        'transactions': transactions,
    }
    return render(request, 'manage_trans.html', context)


@user_passes_test(lambda u: u.is_admin)
def approve_trans(request, transaction_id):
    transaction = get_object_or_404(OAStransaction, id=transaction_id)
    
    if request.method == 'POST':
        amount = Decimal(transaction.amount)
        transaction.approved = True
        transaction.second_user.balance += amount
        transaction.save()
        transaction.second_user.save()

        OAStransaction.objects.create(
                main_user=transaction.second_user,
                second_user=transaction.main_user,
                transaction_type='RECEIVE',
                amount=amount,
                timestamp=timezone.now()
            )
        
        messages.success(request, 'Transaction approved successfully.')
        return redirect('manage_trans')
    

@user_passes_test(lambda u: u.is_admin)
def decline_trans(request, transaction_id):
    transaction = get_object_or_404(OAStransaction, id=transaction_id)
    
    if request.method == 'POST':
        amount = Decimal(transaction.amount)
        transaction.rejected = True
        transaction.main_user.balance += amount
        transaction.save()
        transaction.main_user.save()

        OAStransaction.objects.create(
                main_user=transaction.main_user,
                second_user=transaction.main_user,
                transaction_type='REFUND',
                amount=amount,
                timestamp=timezone.now()
            )
        
        messages.success(request, 'Transaction declined successfully.')
        return redirect('manage_trans')
    

@user_passes_test(lambda u: u.is_admin)
def manage_report(request):
    query = request.GET.get('q', '')
    selected_category = request.GET.get('category', '')

    reports = OASreport.objects.all()

    if query:
        reports = reports.filter(title__icontains=query)

    if selected_category:
        reports = reports.filter(category=selected_category)

    context = {
        'reports': reports,
        'query': query,
        'selected_category': selected_category,
        'categories': [
            'Fraud & Scam', 'Bugs Report', 'Other'
        ],
    }
    return render(request, 'manage_report.html', context)


@user_passes_test(lambda u: u.is_admin)
def delete_report(request, report_id):
    report = get_object_or_404(OASreport, id=report_id)
    
    if request.method == 'POST':
        report.delete()
        messages.success(request, 'Report deleted successfully.')
        return redirect('manage_report')
    

@user_passes_test(lambda u: u.is_admin)
def view_report(request, report_id):
    report = get_object_or_404(OASreport, id=report_id)
    context = {'report': report}
    return render(request, 'view_report.html', context)