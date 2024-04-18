from django import forms
from django.core.exceptions import ValidationError
import re

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
