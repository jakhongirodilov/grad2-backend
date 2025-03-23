from django.db import models
from accounts.models import User


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)


class ReceptivityResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE)
    is_perceived = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)
    is_determined_to_adhere = models.BooleanField(default=False)
    date_created = models.DateTimeField()


class Context(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)

    mood = models.CharField(max_length=100, blank=True, null=True)
#    motivation_rate = models.CharField(max_length=100, blank=True, null=True)
    motivation_rate = models.IntegerField(blank=True, null=True)
    ongoing_activity = models.CharField(max_length=150, blank=True, null=True)
    is_busy = models.BooleanField(default=False)

    surrounding_people = models.CharField(max_length=100, blank=True, null=True)
    surrounding_people_distraction_rate = models.IntegerField(blank=True, null=True)

    location = models.CharField(max_length=100, blank=True, null=True)
    location_distraction_rate = models.IntegerField(blank=True, null=True)

    is_appropriate_time = models.BooleanField(default=True)
    device_type = models.CharField(max_length=100, blank=True, null=True)
    is_silent = models.BooleanField(default=False)
    connection_rate = models.IntegerField(blank=True, null=True)

    work_hours = models.IntegerField(blank=True, null=True)
    sleep_hours = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Context for {self.user} - Notification {self.notification.id}"
