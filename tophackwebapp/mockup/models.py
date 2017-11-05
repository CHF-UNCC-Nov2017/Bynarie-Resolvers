from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import Model
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    options = models.TextField(null=True, default='["accounts"]')
    yodlee_login = models.CharField(max_length=50, default='')
    yodlee_password = models.CharField(max_length=50, default='')

    is_customer = models.BooleanField(default=True)

    ethereum_address = models.CharField(max_length=50, default='')

    def __str__(self):
        return f'{self.user.username} profile {self.options}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
