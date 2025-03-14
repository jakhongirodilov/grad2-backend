import random, datetime
from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from data.utils import send_telegram_message


User = get_user_model()


FORM_SCHEDULE = [
    (("04:55", "05:30"), "https://forms.gle/form1"),
    (("06:55", "70:30"), "https://forms.gle/form2"),
    (("08:55", "9:030"), "https://forms.gle/form3"),
    (("10:55", "11:30"), "https://forms.gle/form4"),
]

MESSAGES = [
    "🚀 Time to move! Take a short break and complete today’s activity. \n✅ Fill out the form:\n\n{form_url}",
    "💡 Small actions, big impact! A little movement now can make a huge difference. Complete today’s activity and let us know how you did! \n🌟 Submit here:\n\n{form_url}",
    "🏆 Every step counts! Stay consistent and complete today’s small task. Keep track of your progress here! \n🎯 Take action now:\n\n{form_url}"
]


def get_current_form():
    """Returns the correct Google Form URL if the current time falls within a range."""
    now = datetime.datetime.utcnow().strftime("%H:%M")
    print(now)

    for (start_time, end_time), form_url in FORM_SCHEDULE:
        print(start_time, now, end_time)
        if start_time <= now <= end_time:
            return form_url

    return None


@csrf_exempt
def notify_user(request, user_id):
    bot_token = '8187229531:AAFlGG2TcUgHiNDkqDPOaDtlZJCj2wGXBxs'
    form_url = get_current_form()

    if not form_url:
        return JsonResponse({"status": "error", "message": "No scheduled form for this time range."})

    msg = random.choice(MESSAGES).format(form_url=form_url)
    response = send_telegram_message(msg, bot_token, user_id)

    if response.get("ok") and "result" in response:
        return JsonResponse({"status": "success", "message": "Notification sent", "response": response})
    else:
        return JsonResponse({"status": "error", "message": "Failed to send notification", "response": response})


@method_decorator(csrf_exempt, name='dispatch')
class SubmitResponseView(APIView):
    def post(self, request):
        pass
    