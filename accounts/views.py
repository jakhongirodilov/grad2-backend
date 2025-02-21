from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .seralizers import UserSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie


User = get_user_model()


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"message": "CSRF token set"})


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
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
    
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"})

@method_decorator(csrf_exempt, name='dispatch')
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

@method_decorator(csrf_exempt, name='dispatch')
class UpdatePlayerIDView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        request.user.one_signal_player_id = request.data.get("player_id")
        request.user.save()
        return Response({"message": "Player ID updated successfully"})