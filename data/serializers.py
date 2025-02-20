from rest_framework import serializers
from .models import Notification, ReceptivityResponse


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class ReceptivityResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceptivityResponse
        fields = '__all__'