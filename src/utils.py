# Утиліти для роботи з даними користувачів

user_profiles = {}

def save_user_to_memory(user_id, user_data):
    user_profiles[user_id] = user_data

def get_telegram_username(update):
    user = update.message.from_user
    return user.username if user.username else 'N/A'

def get_profiles_by_city_and_age(city, min_age, max_age, exclude_user_id):
    return [
        profile for uid, profile in user_profiles.items()
        if uid != exclude_user_id and profile['city'].lower() == city.lower() and min_age <= int(profile['age']) <= max_age
    ]
