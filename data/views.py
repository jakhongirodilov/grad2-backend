from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from data.utils import send_telegram_message


User = get_user_model()


@csrf_exempt
def notify_user(request, user_id):
    bot_token='8187229531:AAFlGG2TcUgHiNDkqDPOaDtlZJCj2wGXBxs'
    msg = 'TEST TEST TEST'

    response = send_telegram_message(msg, bot_token, user_id)

    if response.get("ok") and "result" in response:
        return JsonResponse({"status": "success", "message": "Notification sent", "response": response})
    else:
        return JsonResponse({"status": "error", "message": "Failed to send notification", "response": response})
     


@method_decorator(csrf_exempt, name='dispatch')
class SubmitResponseView(APIView):
    def post(self, request):
        pass
    