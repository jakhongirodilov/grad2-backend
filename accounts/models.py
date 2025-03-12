from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    work_hours = models.IntegerField(default=8)
    sleep_hours = models.FloatField(default=7.0)
    telegram_id = models.CharField(max_length=255, blank=True, null=True)
