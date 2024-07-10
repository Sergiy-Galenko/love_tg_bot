import random
import string

def generate_unique_key() -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(12))

def get_currency(language_code: str) -> str:
    if language_code == "uk":
        return "UAH"
    elif language_code == "us":
        return "USD"
    else:
        return "USD"

def get_subscription_benefits(duration: str, currency: str) -> str:
    if duration == "На тиждень":
        return f"Підписка на тиждень коштує 50 {currency}. Переваги: доступ до 18+ розділу, можливість переглядати профілі без обмежень."
    elif duration == "На місяць":
        return f"Підписка на місяць коштує 150 {currency}. Переваги: доступ до 18+ розділу, можливість переглядати профілі без обмежень."
    elif duration == "На рік":
        return f"Підписка на рік коштує 1000 {currency}. Переваги: доступ до 18+ розділу, можливість переглядати профілі без обмежень, можливість налаштовувати діапазон віку для пошуку."
    else:
        return "Невідомий період підписки."

def search_profiles_by_criteria(user_profiles, city, min_age, max_age, search_preference, is_adult):
    return [
        profile for uid, profile in user_profiles.items()
        if profile['city'] == city
        and min_age <= profile['age'] <= max_age
        and profile.get('is_adult', False) == is_adult
        and (search_preference == "Шукати всіх" or profile['gender'] == search_preference)
    ]
