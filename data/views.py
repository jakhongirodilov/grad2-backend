import random
from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from data.utils import send_telegram_message


User = get_user_model()


@csrf_exempt
def notify_user(request, user_id):
    bot_token = '8187229531:AAFlGG2TcUgHiNDkqDPOaDtlZJCj2wGXBxs'
    
    # List of notification messages
    messages = [
        "🚀 Time to move! Take a quick break and complete today’s activity. \n✅ Submit here:\n\nhttps://forms.gle/sD4j2FPcYBpZche76",
        "💡 Small actions, big impact! A little movement goes a long way. \n🌟 Log your progress:\n\nhttps://forms.gle/sD4j2FPcYBpZche76",
        "🏆 Every step counts! Stay consistent and complete today’s task. \n🎯 Track here:\n\nhttps://forms.gle/sD4j2FPcYBpZche76"
    ]


    # Randomly select a message
    msg = random.choice(messages)

    # Send the message via Telegram
    response = send_telegram_message(msg, bot_token, user_id)

    if response.get("ok") and "result" in response:
        return JsonResponse({"status": "success", "message": "Notification sent", "response": response})
    else:
        return JsonResponse({"status": "error", "message": "Failed to send notification", "response": response})
     


@method_decorator(csrf_exempt, name='dispatch')
class SubmitResponseView(APIView):
    def post(self, request):
        pass
    