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
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class SubmitResponseView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="notification_id",
                description="ID of the notification being responded to",
                required=True,
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
            ),
        ],
        request=ReceptivityResponseSerializer,  
        responses={
            200: {"description": "Response recorded", "example": {"message": "Response recorded"}},
            400: {"description": "Validation Error", "example": {"error": "Invalid data"}},
        },
    )
    
    def post(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id)
        serializer = ReceptivityResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=notification.user, notification=notification)
            return Response({"message": "Response recorded"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from django.http import JsonResponse
from data.utils import send_telegram_message

@csrf_exempt
def notify_user(request, user_id):
    bot_token='8187229531:AAFlGG2TcUgHiNDkqDPOaDtlZJCj2wGXBxs'
    msg = 'TEST TEST TEST'
    response = send_telegram_message(msg, bot_token, user_id)
    return JsonResponse(response)
