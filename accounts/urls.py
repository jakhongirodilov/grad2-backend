from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user-profile/', UserProfileView.as_view(), name='user_profile'),
    path('update-player-id/', UpdatePlayerIDView.as_view(), name='update_player_id'),
    path("get-csrf-token/", get_csrf_token),
]