from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager

class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


    def __str__(self):
        return self.email