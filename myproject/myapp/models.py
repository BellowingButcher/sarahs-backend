from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    is_teamleader = models.BooleanField(default=False)
    is_teammember = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Schedules(models.Model):
    schedule = models.URLField(default=None)
    uploaded_by = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    beginning = models.DateTimeField(auto_now=False, auto_now_add=False, unique=True)
    ending = models.DateTimeField(auto_now=False, auto_now_add=False, unique=True)
    status = models.BooleanField(default=True)


class UserSchedules(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    schedule = models.ForeignKey('Schedules', on_delete=models.CASCADE)
