from django.contrib import admin
from home_page.models import OASuser
# Register your models here.

class OASuserAdmin(admin.ModelAdmin):
    list_display = ['username', 'password', 'first_name', 'last_name', 'date_of_birth', 'gender', 'phone_number', 'email', 'address']

admin.site.register(OASuser, OASuserAdmin)