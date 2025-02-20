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
    location = models.CharField(max_length=50, choices=[('home', 'Home'), ('work', 'Work'), ('study', 'Study'), ('other', 'Other')])
    mood = models.CharField(max_length=50, choices=[('happy', 'Happy'), ('neutral', 'Neutral'), ('stressed', 'Stressed')])
    social_environment = models.CharField(max_length=50, choices=[('alone', 'Alone'), ('with friends', 'With Friends'), ('in public', 'In Public')])
    is_busy = models.BooleanField()
