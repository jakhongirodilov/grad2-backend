import random, os, datetime, logging
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from data.utils import send_telegram_message, import_receptivity, import_context
from data.models import Notification


User = get_user_model()


DATASET_DIR = os.path.join(settings.BASE_DIR, "dataset")


# Setup logging
LOG_FILE = "notifications.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

FORM_SCHEDULE = [
    (("04:55", "05:30"), "https://forms.gle/C1KuHNPPuQGfPfnJ6", "https://forms.gle/HXVHfLJULXs5FQnz6"),
    (("06:55", "07:30"), "https://forms.gle/TwD8DrSP9MLH385V9", "https://forms.gle/LpkJHQgAjXnxuyrz8"),
    (("08:55", "09:30"), "https://forms.gle/eofts8bc8SE7fmGMA", "https://forms.gle/i1AbRAqnNFPy8MsNA"),
    (("10:55", "11:30"), "https://forms.gle/Km4hEfP3zWAsxFtZ6", "https://forms.gle/XVpWUxgPPR3dqrgj7"),
]

MESSAGES = [
    "🚀 Time to move! Take a short break and complete today’s activity.\n\n✅ Task: {task_url}\n\n\n📝 Context: {context_url}",
    "🏆 Stay active! Complete today’s task and keep the momentum going.\n\n🎯 Task: {task_url}\n\n\n📝 Context: {context_url}",
    "🔥 Quick break time! Refresh your body and mind.\n\n✅ Task: {task_url}\n\n\n📝 Context: {context_url}"
]


def get_current_form():
    """Returns the correct Google Form URL if the current time falls within a range."""
    now = datetime.datetime.utcnow().strftime("%H:%M")
    
    for (start_time, end_time), task_url, context_url in FORM_SCHEDULE:
        if start_time <= now <= end_time:
            print(task_url, context_url)
            return task_url, context_url

    return None, None



@csrf_exempt
def notify_user(request):
    bot_token = '8187229531:AAFlGG2TcUgHiNDkqDPOaDtlZJCj2wGXBxs'
    
    task_url, context_url = get_current_form()
    if not task_url:
        logging.warning("No scheduled form for this time range.")
        return JsonResponse({"status": "error", "message": "No scheduled form for this time range."})

    users = User.objects.exclude(telegram_id__isnull=True).exclude(telegram_id="")
    if not users.exists():
        logging.warning("No users with Telegram IDs found.")
        return JsonResponse({"status": "error", "message": "No users with Telegram IDs found."})

    msg = random.choice(MESSAGES).format(task_url=task_url, context_url=context_url)
    
    sent_notifications = []
    failed_notifications = []

    for user in users:
        response = send_telegram_message(msg, bot_token, user.telegram_id)
        is_sent = response.get("ok") and "result" in response

        # Create notification object
        notification = Notification.objects.create(user=user, is_sent=is_sent)

        if is_sent:
            sent_notifications.append(notification.id)
            logging.info(f"Notification {notification.id} sent to {user.username}.")
        else:
            failed_notifications.append(notification.id)
            logging.error(f"Failed to send Notification {notification.id} to {user.username}.\n  Response: {response}")

    return JsonResponse({
        "status": "success" if sent_notifications else "error",
        "message": f"Notifications sent to {len(sent_notifications)} users, failed for {len(failed_notifications)} users.",
        "sent_notifications": sent_notifications,
        "failed_notifications": failed_notifications
    })


@csrf_exempt
def import_data(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)

    try:
        receptivity_file = os.path.join(DATASET_DIR, "receptivity_2025-03-15.csv")
        context_file = os.path.join(DATASET_DIR, "context_2025-03-15.csv")

        if os.path.exists(receptivity_file):
            import_receptivity(receptivity_file)

        if os.path.exists(context_file):
            import_context(context_file)

        return JsonResponse({"message": "Data imported successfully."}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class SubmitResponseView(APIView):
    def post(self, request):
        pass
    