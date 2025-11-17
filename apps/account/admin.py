from django.contrib import admin

# Register your models here.
from apps.account.models import *


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone_number','balance_of_user', 'is_active', 'date_joined', 'rate']
    list_filter = ['is_active', 'date_joined', 'country']
    search_fields = ['username']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Country)
