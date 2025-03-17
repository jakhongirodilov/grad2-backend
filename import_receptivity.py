import csv
import pytz
from datetime import datetime
from django.utils.timezone import make_aware
from data.models import ReceptivityResponse, Notification
from django.contrib.auth import get_user_model

User = get_user_model()

CSV_FILE_PATH = "data.csv" 

def import_receptivity_data():
    with open(CSV_FILE_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            # Convert date_created to UTC
            local_tz = pytz.timezone("Asia/Tashkent")  # Since your timestamps have +05:00
            local_dt = datetime.strptime(row["date_created"], "%Y-%m-%dT%H:%M:%S.%f%z")
            utc_dt = local_dt.astimezone(pytz.UTC)  # Convert to UTC
            
            try:
                user = User.objects.get(id=row["user_id"])
                notification = Notification.objects.get(id=row["notification_id"])
                
                # Create and save ReceptivityResponse entry
                ReceptivityResponse.objects.create(
                    user=user,
                    notification=notification,
                    is_perceived=row["is_perceived"].lower() == "true",
                    is_available=row["is_available"].lower() == "true",
                    is_determined_to_adhere=row["is_determined_to_adhere"].lower() == "true",
                    date_created=utc_dt
                )
                print(f"Saved response for user {user.id}, notification {notification.id}")

            except User.DoesNotExist:
                print(f"User {row['user_id']} not found, skipping...")
            except Notification.DoesNotExist:
                print(f"Notification {row['notification_id']} not found, skipping...")

if __name__ == "__main__":
    import_receptivity_data()
