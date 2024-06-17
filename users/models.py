from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)

# Create your models here 


class UserManager(BaseUserManager):

    """ 
    Object Manager for User model.
    
    Supports the following operations:

        1. Creating users
        2. Email validation
    """


    def create_user(self, email, first_name, last_name, password, **extra_fields):
        
        """Creates user using email, password and additional fields"""        

        if not email:
            raise ValueError('Email is required, please enter your email')
        
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name, 
            last_name=last_name, 
            **extra_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        
        """Creates admin user using email, password and additional fields"""

        user = self.create_user(email, first_name, last_name, password, **extra_fields)
        
        user.is_superuser = True
        user.is_active = True
        user.is_verified = True
        user.is_staff = True 

        user.save(using=self._db)
        
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    
    """Base User Model"""

    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['first_name', 'last_name']


    def __str__(self) -> str:
        return self.email
    