from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The phone_number must be set'))
        
        
        # Ensure CNIC and other required fields are always present
        if 'cnic' not in extra_fields or not extra_fields['cnic']:
            extra_fields['cnic'] = f"default_cnic_{self.model.objects.count()+1}"  # Generate a unique default CNIC
            
    
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        # Provide default values for required fields
        extra_fields.setdefault('cnic', f"default_cnic_{self.model.objects.count()+1}")
        # extra_fields.setdefault('first_name', 'Admin')
        # extra_fields.setdefault('last_name', 'User')
        # extra_fields.setdefault('phone_number', '0000000000')
        # extra_fields.setdefault('address', 'Admin Address')
        
        return self.create_user(email, password, **extra_fields)