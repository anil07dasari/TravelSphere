import uuid
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from accounts.managers import CustomUserManager


class CustomUser(AbstractUser):
    RENTAL = 'Rental'
    CUSTOMER = 'Customer'
    ROLES = (
        (RENTAL, _('Rental')),
        (CUSTOMER, _('Customer')),
    )
    username = None
    user_uuid = models.UUIDField(default=uuid.uuid4, editable=False, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True, unique=True)
    cnic = models.CharField(max_length=30, unique=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True, unique=True)
    address = models.TextField()
    image = models.ImageField(upload_to="Customer", null=True)
    created_at = models.DateField(null=True, blank=True, auto_now=True, editable=True)
    roles = models.CharField(max_length=50, choices=ROLES, default=RENTAL)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'  
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email  