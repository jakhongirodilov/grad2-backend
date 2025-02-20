from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    work_hours = models.IntegerField(default=8)
    sleep_hours = models.FloatField(default=7.0)
    one_signal_player_id = models.CharField(max_length=255, blank=True, null=True)

