from django.db import models
from django.conf import settings

from accounts.models import CustomUser

class Brand(models.Model):
    brand_name = models.CharField(max_length=255)

class Car_type(models.TextChoices):
    MANUAL = 'M', 'Manual'
    AUTO = 'A', 'Auto'
    HYBRID = 'H', 'Hybrid'
    
class Car(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    car_brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    car_model = models.CharField(max_length=100, null=True)
    seats = models.CharField(max_length=100, null=True)
    type = models.CharField(
        max_length=1, 
        choices=Car_type.choices,
        default=Car_type.MANUAL
    )
    price_per_day = models.PositiveSmallIntegerField(default=0)
    location = models.CharField(max_length=255)
    licence_plate_no = models.CharField(max_length=50, null=True)
    image = models.ImageField(upload_to="car", null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")  # ✅ Added status


    def __str__(self):
        return self.type


class Status(models.TextChoices):
    PENDING = 'P', 'Pending'
    APPROVED = 'A', 'Approved'
    CANCELLED = 'C', 'Cancelled'
    PAID = 'S', 'PAID'



class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="bookings")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="car")
    customer_first_name = models.CharField(max_length=100)
    customer_last_name = models.CharField(max_length=100)
    total_price = models.PositiveSmallIntegerField(default=0)
    address = models.TextField()
    cnic = models.CharField(max_length=15)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    from_date = models.DateField()
    to_date = models.DateField()
    status = models.CharField(
        max_length=1, 
        choices=Status.choices, 
        default=Status.PENDING
    )

    def __str__(self):
        return self.status
    

    def save(self, *args, **kwargs):
        """Calculate the total price before saving the booking."""
        if self.from_date and self.to_date and self.car:
            print(self.from_date, 'Form', self.to_date, 'TO')
            number_of_days = max(1, (self.to_date - self.from_date).days)  # Ensure at least 1 day
            print(number_of_days)
            self.total_price = number_of_days * self.car.price_per_day  # Calculate total price

        super().save(*args, **kwargs)