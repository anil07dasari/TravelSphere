from django.contrib import admin
from accounts.models import CustomUser

# Register your models here.

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'phone_number')
    search_fields = ('email', 'phone_number')