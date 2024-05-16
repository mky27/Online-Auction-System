import datetime
from django.db import models
from django.contrib.auth.hashers import check_password as check_password_hash
from django.contrib.auth.hashers import make_password
from django.core.validators import MinValueValidator

class OASuser(models.Model):
    username = models.CharField(max_length=20, unique=True)
    userPass = models.CharField(max_length=255)
    fName = models.CharField(max_length=50)
    lName = models.CharField(max_length=50)
    date_of_birth = models.DateField(default=datetime.date.today)
    gender = models.CharField(max_length=10)
    phoneNo = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    ratings = models.DecimalField(max_digits=65, decimal_places=1, blank=True, null=True)
 
    def __str__(self):
        return self.username
    
    def check_password(self, raw_password):
        return check_password_hash(raw_password, self.userPass)

    def get_username(self):
        """
        Return the username of the user.
        """
        return self.username

    @property
    def is_authenticated(self):
        return self.is_active
    
    def set_password(self, raw_password):
        self.userPass = make_password(raw_password)

class OASauction(models.Model):
    item_name = models.CharField(max_length=50)
    item_desc = models.TextField(max_length=100)
    item_cat = models.CharField(max_length=50)
    start_bid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=start_bid)
    second_highest_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    current_bidder = models.ForeignKey(OASuser, on_delete=models.SET_NULL, null=True, blank=True, related_name='bidding_auctions')
    second_highest_bidder = models.ForeignKey(OASuser, on_delete=models.SET_NULL, null=True, blank=True)
    seller = models.ForeignKey(OASuser, on_delete=models.CASCADE, related_name='seller_auctions')
    auction_created_time = models.DateTimeField(null=True, blank=True)
    auction_end_time = models.DateTimeField()
    comment = models.TextField(blank=True, null=True)
    picture1 = models.ImageField(upload_to='auction_pictures/', blank=True, null=True)
    picture2 = models.ImageField(upload_to='auction_pictures/', blank=True, null=True)
    picture3 = models.ImageField(upload_to='auction_pictures/', blank=True, null=True)
    picture4 = models.ImageField(upload_to='auction_pictures/', blank=True, null=True)
    picture5 = models.ImageField(upload_to='auction_pictures/', blank=True, null=True)
    picture6 = models.ImageField(upload_to='auction_pictures/', blank=True, null=True)
    picture7 = models.ImageField(upload_to='auction_pictures/', blank=True, null=True)
    is_saved = models.BooleanField(default=False)
    is_ongoing = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.item_name
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.current_bid = self.start_bid
        super().save(*args, **kwargs)

class OASwatchlist(models.Model):
    user = models.ForeignKey(OASuser, on_delete=models.CASCADE)
    auction = models.ForeignKey(OASauction, on_delete=models.CASCADE)

class OASauctionWinner(models.Model):
    auction = models.OneToOneField(OASauction, on_delete=models.CASCADE)
    winner = models.ForeignKey(OASuser, on_delete=models.CASCADE)
    winning_bid = models.DecimalField(max_digits=10, decimal_places=2)
    buyer_name = models.CharField(max_length=100, blank=True, null=True)
    buyer_phone = models.CharField(max_length=15, blank=True, null=True)
    buyer_address = models.TextField(blank=True, null=True)
    is_checkout = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    is_received = models.BooleanField(default=False)

    # python manage.py makemigrations
    # python manage.py migrate

    # python manage.py runserver

    # python manage.py shell
    # from home_page.models import OASuser
    # OASuser.objects.all()
    