from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import DecimalValidator
from django.utils import timezone
import re

def my_view(request):
    timezone.activate('UTC')

def validate_username(value):
    if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,20}$', value):
        raise ValidationError(
            'Username must be between 6-20 characters and contain at least 1 letter and 1 number.'
        )

class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='Username ', max_length=20, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    userPass = forms.CharField(label='Password ', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password ', widget=forms.PasswordInput())

class PersonalInfoForm(forms.Form):
    fName = forms.CharField(label='First Name ', max_length=50, widget=forms.TextInput(attrs={'class': 'name-field', 'autocomplete': 'off'}))
    lName = forms.CharField(label='Last Name ', max_length=50, widget=forms.TextInput(attrs={'class': 'name-field', 'autocomplete': 'off'}))
    date_of_birth = forms.DateField(label='Date of Birth ', widget=forms.DateInput(attrs={'class': 'dob-phoneNo-field', 'autocomplete': 'off'}))
    gender = forms.ChoiceField(label='Gender ', choices=[('Male', 'Male'), ('Female', 'Female')], widget=forms.Select(attrs={'class': 'gender-field'}))
    phoneNo = forms.CharField(label='Phone Number ', max_length=20, widget=forms.TextInput(attrs={'class': 'dob-phoneNo-field', 'autocomplete': 'off'}))
    email = forms.EmailField(label='Email ', widget=forms.EmailInput(attrs={'class': 'email-field', 'autocomplete': 'off'}))
    address = forms.CharField(label='Address ', widget=forms.Textarea(attrs={'class': 'address-field', 'autocomplete': 'off'}))

class LoginForm(forms.Form):
    username = forms.CharField(label='Username ', max_length=20, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    userPass = forms.CharField(label='Password ', widget=forms.PasswordInput())

class ForgotPassForm(forms.Form):
    username = forms.CharField(label='Username ', max_length=20, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    email = forms.EmailField(label='Email ')

class ResetPassForm(forms.Form):
    userPass = forms.CharField(label='New Password ', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password ', widget=forms.PasswordInput())

class EditProfileForm(forms.Form):
    fName = forms.CharField(label='First Name ', max_length=50, widget=forms.TextInput(attrs={'class': 'name-field', 'autocomplete': 'off'}))
    lName = forms.CharField(label='Last Name ', max_length=50, widget=forms.TextInput(attrs={'class': 'name-field', 'autocomplete': 'off'}))
    date_of_birth = forms.DateField(label='Date of Birth ', widget=forms.DateInput(attrs={'class': 'dob-phoneNo-field', 'autocomplete': 'off'}))
    gender = forms.ChoiceField(label='Gender ', choices=[('Male', 'Male'), ('Female', 'Female')], widget=forms.Select(attrs={'class': 'gender-field'}))
    phoneNo = forms.CharField(label='Phone Number ', max_length=20, widget=forms.TextInput(attrs={'class': 'dob-phoneNo-field', 'autocomplete': 'off'}))
    email = forms.EmailField(label='Email ', widget=forms.EmailInput(attrs={'class': 'email-field', 'autocomplete': 'off'}))
    address = forms.CharField(label='Address ', widget=forms.Textarea(attrs={'class': 'address-field', 'autocomplete': 'off'}))

class CreateAuctionForm(forms.Form):
    item_name = forms.CharField(label='Item Name ', max_length=50, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    item_desc = forms.CharField(label='Item Description ', max_length=100, widget=forms.Textarea(attrs={}))
    item_cat = forms.ChoiceField(label='Item Category ', choices=[('Apparel & Accessories', 'Apparel & Accessories'), ('Animal & Pet Supplies', 'Animal & Pet Supplies'),
                                                                  ('Arts & Entertainment', 'Arts & Entertainment'), ('Baby & Toddler', 'Baby & Toddler'),
                                                                  ('Camera & Optics', 'Camera & Optics'), ('Electronics', 'Electronics'), ('Food & Beverages', 'Food & Beverages'),
                                                                  ('Furniture', 'Furniture'), ('Hardware', 'Hardware'), ('Home & Garden', 'Home & Garden'), 
                                                                  ('Health & Beauty', 'Health & Beauty'), ('Luggage & Bags', 'Luggage & Bags'), ('Office Supplies', 'Office Supplies'),
                                                                  ('Religious', 'Religious'), ('Sporting Goods', 'Sporting Goods'), ('Toys & Games', 'Toys & Games'),
                                                                  ('Vehicle & Parts', 'Vehicle & Parts'), ('Others', 'Others')
                                                                  ], widget=forms.Select(attrs={}))
    start_bid = forms.DecimalField(label='Starting Bid ', max_digits=10, decimal_places=2, min_value=1)
    auction_end_time = forms.DateTimeField(label='End Time ', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    picture1 = forms.ImageField()
    picture2 = forms.ImageField()
    picture3 = forms.ImageField()
    picture4 = forms.ImageField()
    picture5 = forms.ImageField(required=False)
    picture6 = forms.ImageField(required=False)
    picture7 = forms.ImageField(required=False)

    def clean_start_bid(self):
        start_bid = self.cleaned_data['start_bid']
        try:
            DecimalValidator(max_digits=10, decimal_places=2)(start_bid)
        except ValidationError:
            raise ValidationError('Starting bid must be a valid decimal number.')
        return start_bid
    
    def clean_auction_end_time(self):
        auction_end_time = self.cleaned_data.get('auction_end_time')
        if auction_end_time <= timezone.now():
            raise forms.ValidationError("Auction end time must be in the future.")
        return auction_end_time

class PlaceBidForm(forms.Form):
    bid_amount = forms.DecimalField(label='Bid Amount', min_value=0, max_digits=10, decimal_places=2)

class EditAuctionForm(forms.Form):
    item_name = forms.CharField(label='Item Name ', max_length=50, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    item_desc = forms.CharField(label='Item Description ', max_length=100, widget=forms.Textarea(attrs={}))
    item_cat = forms.ChoiceField(label='Item Category ', choices=[('Apparel & Accessories', 'Apparel & Accessories'), ('Animal & Pet Supplies', 'Animal & Pet Supplies'),
                                                                  ('Arts & Entertainment', 'Arts & Entertainment'), ('Baby & Toddler', 'Baby & Toddler'),
                                                                  ('Camera & Optics', 'Camera & Optics'), ('Electronics', 'Electronics'), ('Food & Beverages', 'Food & Beverages'),
                                                                  ('Furniture', 'Furniture'), ('Hardware', 'Hardware'), ('Home & Garden', 'Home & Garden'), 
                                                                  ('Health & Beauty', 'Health & Beauty'), ('Luggage & Bags', 'Luggage & Bags'), ('Office Supplies', 'Office Supplies'),
                                                                  ('Religious', 'Religious'), ('Sporting Goods', 'Sporting Goods'), ('Toys & Games', 'Toys & Games'),
                                                                  ('Vehicle & Parts', 'Vehicle & Parts'), ('Others', 'Others')
                                                                  ], widget=forms.Select(attrs={}))
    start_bid = forms.DecimalField(label='Starting Bid ', max_digits=10, decimal_places=2, min_value=1)
    auction_end_time = forms.DateTimeField(label='End Time ', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    picture1 = forms.ImageField(required=False)
    picture2 = forms.ImageField(required=False)
    picture3 = forms.ImageField(required=False)
    picture4 = forms.ImageField(required=False)
    picture5 = forms.ImageField(required=False)
    picture6 = forms.ImageField(required=False)
    picture7 = forms.ImageField(required=False)

    def clean_start_bid(self):
        start_bid = self.cleaned_data['start_bid']
        try:
            DecimalValidator(max_digits=10, decimal_places=2)(start_bid)
        except ValidationError:
            raise ValidationError('Starting bid must be a valid decimal number.')
        return start_bid
    
    def clean_auction_end_time(self):
        auction_end_time = self.cleaned_data.get('auction_end_time')
        if auction_end_time <= timezone.now():
            raise forms.ValidationError("Auction end time must be in the future.")
        return auction_end_time

class ChangePasswordForm(forms.Form):
    email = forms.EmailField(label='Email')
    current_password = forms.CharField(label='Current Password', widget=forms.PasswordInput)
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
