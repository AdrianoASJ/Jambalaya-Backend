from django.contrib import admin
from .models import *

admin.site.site_header = 'Jambalaya'


class AccountAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "city"]


admin.site.register(Account, AccountAdmin)