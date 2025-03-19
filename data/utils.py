import requests, csv, pytz
from datetime import datetime
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_datetime
from django.core.exceptions import ValidationError

from .models import Notification, ReceptivityResponse, Context


User = get_user_model()


TELEGRAM_BOT_TOKEN = '8187229531:AAFlGG2TcUgHiNDkqDPOaDtlZJCj2wGXBxs'
CHAT_ID = '5563104704'

def send_telegram_message(message, bot_token, user_id):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        "chat_id": user_id,
        "text": message,
        "parse_mode": "Markdown",
    }
    response = requests.post(url, json=payload)
    return response.json()


UTC_TZ = pytz.UTC  

def import_receptivity(file_path):
    """Import receptivity data from CSV and store timestamps in UTC."""
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            try:
                # Convert date_created to UTC
                local_dt = parse_datetime(row["date_created"])  # Parses timezone automatically
                if local_dt is None:
                    raise ValidationError("Invalid datetime format.")
                
                utc_dt = local_dt.astimezone(UTC_TZ)  # Convert to UTC

                # Fetch user and notification
                user = User.objects.get(id=row["user_id"])
                notification = Notification.objects.get(id=row["notification_id"])

                # Save response
                ReceptivityResponse.objects.create(
                    user=user,
                    notification=notification,
                    is_perceived=row["is_perceived"].lower() == "true",
                    is_available=row["is_available"].lower() == "true",
                    is_determined_to_adhere=row["is_determined_to_adhere"].lower() == "true",
                    date_created=utc_dt
                )
                print(f"✅ Saved response for user {user.id}, notification {notification.id}")

            except User.DoesNotExist:
                print(f"⚠️ User {row['user_id']} not found, skipping...")
            except Notification.DoesNotExist:
                print(f"⚠️ Notification {row['notification_id']} not found, skipping...")
            except ValidationError as e:
                print(f"⚠️ Skipping row due to validation error: {e}")
            except Exception as e:
                print(f"❌ Unexpected error: {e}")


def import_context(file_path):
    """Import context data from CSV and store in the database."""
    User = get_user_model()
    
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # Skip empty rows
            if not row['user_id'] or not row['notification_id']:
                print("⚠️ Skipping row with missing user_id or notification_id")
                continue
            
            try:
                user = User.objects.get(id=row['user_id'])
                notification = Notification.objects.get(id=row['notification_id'])

                context = Context(
                    user=user,
                    notification=notification,
                    mood=row.get("mood", ""),
                    motivation_rate=row.get("motivation_rate", ""),
                    ongoing_activity=row.get("ongoing_activity", ""),
                    is_busy=row.get("is_busy", "").lower() == "true",
                    
                    surrounding_people=row.get("surrounding_people", ""),
                    surrounding_people_distraction_rate=int(row["surrounding_people_distraction_rate"]) if row.get("surrounding_people_distraction_rate") else None,
                    
                    location=row.get("location", ""),
                    location_distraction_rate=int(row["location_distraction_rate"]) if row.get("location_distraction_rate") else None,
                    
                    is_appropriate_time=row.get("is_appropriate_time", "").lower() == "true",
                    device_type=row.get("device_type", ""),
                    is_silent=row.get("is_silent", "").lower() == "true",
                    connection_rate=int(row["connection_rate"]) if row.get("connection_rate") else None,
                    
                    work_hours=int(row["work_hours"]) if row.get("work_hours") else None,
                    sleep_hours=int(row["sleep_hours"]) if row.get("sleep_hours") else None,
                )
                context.save()
                print(f"✅ Saved context for user {user.id}, notification {notification.id}")
            
            except User.DoesNotExist:
                print(f"⚠️ User {row['user_id']} not found, skipping...")
            except Notification.DoesNotExist:
                print(f"⚠️ Notification {row['notification_id']} not found, skipping...")
            except ValueError as e:
                print(f"⚠️ Skipping row due to value error: {e}")
            except ValidationError as e:
                print(f"⚠️ Skipping row due to validation error: {e}")
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
