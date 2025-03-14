from django.db import models
from accounts.models import User


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)


class ReceptivityResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=False)
    is_determined_to_adhere = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)


class Context(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=True, null=True)
    work_hours = models.IntegerField(default=8, blank=True, null=True)
    sleep_hours = models.FloatField(default=7.0, blank=True, null=True)
    mood = models.CharField(max_length=100, blank=True, null=True)
    social_environment = models.CharField(max_length=100, blank=True, null=True)
    ongoing_task = models.CharField(max_length=150, blank=True, null=True)
