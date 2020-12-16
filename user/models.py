from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    USER_TYPES = (
        (None, 'Choose your gender'),
        ('Investor', 'Investor'),
        ('Borrower', 'Borrower'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    balance = models.FloatField(default=0)




