from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Notification
from .serializers import ReceptivityResponseSerializer
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class SubmitResponseView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id)
        serializer = ReceptivityResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=notification.user, notification=notification)
            return Response({"message": "Response recorded"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)