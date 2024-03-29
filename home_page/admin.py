from django.contrib import admin
from home_page.models import OASuser
# Register your models here.

class OASuserAdmin(admin.ModelAdmin):
    list_display = ['username', 'userPass']

admin.site.register(OASuser, OASuserAdmin)