from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiExample
from .seralizers import UserSerializer


User = get_user_model()


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"message": "CSRF token set"})


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    @extend_schema(
        request=UserSerializer,
        responses={201: {"message": "User registered successfully"}, 400: "Validation Error"},
    )

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    @extend_schema(
        request=OpenApiTypes.OBJECT,
        examples=[
            OpenApiExample(
                "Login Example",
                summary="Example login request",
                value={"username": "testuser", "password": "securepassword"},
                request_only=True,
            )
        ],
        responses={
            200: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
        },
    )
    
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        return Response({"message": "Login successful"})


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        request=None,
        responses={200: {"message": "Logout successful"}},
    )

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"})


@method_decorator(csrf_exempt, name='dispatch')
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        responses={200: UserSerializer},
    )

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    

@method_decorator(csrf_exempt, name='dispatch')
class UpdatePlayerIDView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        request=OpenApiTypes.OBJECT,
        examples=[
            OpenApiExample(
                "Update Player ID",
                summary="Example request to update OneSignal player ID",
                value={"player_id": "some-unique-id"},
                request_only=True,
            )
        ],
        responses={200: {"message": "Player ID updated successfully"}},
    )

    def post(self, request):
        request.user.telegram_id = request.data.get("player_id")
        request.user.save()
        return Response({"message": "Player ID updated successfully"})