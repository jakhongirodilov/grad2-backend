from django.contrib.auth import get_user_model

User = get_user_model()

users_data = [
    {"username": "2110053@newuu.uz", "telegram_id": "845486735"},
    {"username": "2110057@newuu.uz", "telegram_id": "5563104704"},
    {"username": "2110058@newuu.uz", "telegram_id": "304500307"},
    {"username": "2110074@newuu.uz", "telegram_id": "1208994855"},
    {"username": "2110125@newuu.uz", "telegram_id": "606016081"},
    {"username": "2110155@newuu.uz", "telegram_id": "557223030"},
    {"username": "2110160@newuu.uz", "telegram_id": "1985440957"},
]

for user_data in users_data:
    user, created = User.objects.get_or_create(username=user_data["username"], defaults={"telegram_id": user_data["telegram_id"]})
    if created:
        print(f"User {user.username} created.")
    else:
        print(f"User {user.username} already exists.")
