from django.contrib import admin

from subscription.models import  Payment

# Register your models here.
# @admin.register(SubscriptionPlan)
# class CarAdmin(admin.ModelAdmin):
#     list_display = ['name']
    
@admin.register(Payment)
class CarAdmin(admin.ModelAdmin):
    list_display = ['stripe_checkout_id']