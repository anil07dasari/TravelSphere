from django.db import models
from django.conf import settings
from booking.models import *

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, related_name='payments')
    stripe_checkout_id = models.CharField(max_length=255, unique=True)
    stripe_payment_intent = models.CharField(max_length=255, unique=True, null=True, blank=True)
    status = models.CharField(max_length=50, default="Pending")
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"
