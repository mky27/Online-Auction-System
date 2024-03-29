from django import forms

class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=15)
    userPass = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

class PersonalInfoForm(forms.Form):
    fName = forms.CharField(label='First Name', max_length=50)
    lName = forms.CharField(label='Last Name', max_length=50)
    date_of_birth = forms.DateField(label='Date of Birth')
    gender = forms.ChoiceField(label='Gender', choices=[('Male', 'Male'), ('Female', 'Female')])
    phoneNo = forms.CharField(label='Phone Number', max_length=20)
    email = forms.EmailField(label='Email')
    address = forms.CharField(label='Address', widget=forms.Textarea)

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=15)
    userPass = forms.CharField(label='Password', widget=forms.PasswordInput)
