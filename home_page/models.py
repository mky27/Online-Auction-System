import datetime
from django.db import models

class OASuser(models.Model):
    username = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(default=datetime.date.today)
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
 
    def __str__(self):
        return self.username
    
    # python manage.py shell
    # from home_page.models import OASuser
    # OASuser.objects.all()