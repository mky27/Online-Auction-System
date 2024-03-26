from django.contrib import admin
from home_page.models import OASuser
# Register your models here.

class OASuserAdmin(admin.ModelAdmin):
    list_display = ['username', 'userPass', 'fName', 'lName', 'date_of_birth', 'gender', 'phoneNo', 'email', 'address']

admin.site.register(OASuser, OASuserAdmin)