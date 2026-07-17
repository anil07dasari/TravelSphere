from django.contrib import admin
from .models import Car, Booking, Brand

# Register your models here.

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['car_model']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['car', 'customer_first_name', 'from_date', 'to_date']
    list_filter = ['from_date', 'to_date', 'car']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["brand_name"]