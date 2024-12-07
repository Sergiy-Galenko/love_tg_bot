import random
import string

def generate_unique_key(length=10) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def get_currency(country_code: str) -> str:
    return "грн" if country_code == "uk" else "USD"

def get_subscription_benefits(duration: str, currency: str) -> str:
    benefits = {
        "На тиждень": f"Ціна: 100 {currency}\n- Доступ до 18+\n- Розширені фільтри пошуку",
        "На місяць": f"Ціна: 300 {currency}\n- Доступ до 18+\n- Розширені фільтри пошуку\n- Пріоритетна підтримка",
        "На рік": f"Ціна: 3000 {currency}\n- Доступ до 18+\n- Розширені фільтри пошуку\n- Пріоритетна підтримка\n- Встановлення власного діапазону віку"
    }
    return benefits.get(duration, "Невідомий тип підписки")

def search_profiles_by_criteria(user_profiles, city, min_age, max_age, search_preference, is_adult):
    return [
        profile for uid, profile in user_profiles.items()
        if profile['city'].lower() == city.lower() and
        min_age <= profile['age'] <= max_age and
        (search_preference == "Шукати всіх" or profile['gender'] == search_preference) and
        profile.get('is_adult', False) == is_adult
    ]
