from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.TextField()
    phone = models.CharField(max_length=20)
    is_admin = models.BooleanField(default=False)
    password_reset_token = models.CharField(max_length=100, null=True, blank=True)
    password_reset_method = models.CharField(max_length=50, null=True, blank=True)
    profile_image = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

