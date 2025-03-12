from django.urls import path
from .views import *


urlpatterns = [
    path('submit-response/<int:notification_id>/', SubmitResponseView.as_view(), name='submit_response'),
    path('notify/<int:user_id>/', notify_user, name='notify_user'),
]