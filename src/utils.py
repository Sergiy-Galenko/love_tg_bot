import random
import string

def generate_unique_key(length=10) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def get_currency(user_country: str) -> str:
    # Реалізуйте логіку визначення валюти на основі коду країни
    return "грн"  # Приклад: повертає гривню

def get_subscription_benefits(duration: str, currency: str) -> str:
    if duration == "На тиждень":
        return f"Вартість підписки на тиждень: 50 {currency}.\nПереваги: ... (список переваг)"
    elif duration == "На місяць":
        return f"Вартість підписки на місяць: 150 {currency}.\nПереваги: ... (список переваг)"
    elif duration == "На рік":
        return f"Вартість підписки на рік: 1800 - ?% = 1200{currency}.\nПереваги: ... (список переваг)\n\nДодаткова можливість: вибір діапазону віку для пошуку (від 18 до 99)."
    return ""

def search_profiles_by_criteria(user_profiles: dict, city: str, min_age: int, max_age: int, search_preference: str) -> list:
    matching_profiles = []
    for profile in user_profiles.values():
        if profile['city'] == city and min_age <= profile['age'] <= max_age:
            if search_preference == "Шукати всіх" or profile['gender'] == search_preference:
                matching_profiles.append(profile)
    return matching_profiles
