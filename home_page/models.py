import datetime
from django.db import models
from django.contrib.auth.hashers import check_password as check_password_hash

class OASuser(models.Model):
    username = models.CharField(max_length=15, unique=True)
    userPass = models.CharField(max_length=255)
    fName = models.CharField(max_length=50)
    lName = models.CharField(max_length=50)
    date_of_birth = models.DateField(default=datetime.date.today)
    gender = models.CharField(max_length=10)
    phoneNo = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    last_login = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
 
    def __str__(self):
        return self.username
    
    def check_password(self, raw_password):
        return check_password_hash(raw_password, self.userPass)


    # python manage.py makemigrations
    # python manage.py migrate

    # python manage.py runserver

    # python manage.py shell
    # from home_page.models import OASuser
    # OASuser.objects.all()
    