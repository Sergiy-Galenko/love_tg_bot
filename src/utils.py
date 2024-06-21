import random
import string

def generate_unique_key(length=12):
    characters = string.ascii_letters + string.digits
    key = ''.join(random.choice(characters) for i in range(length))
    return key

def get_currency(country_code):
    currency_dict = {
        "US": "USD",
        "UA": "UAH",
        "EU": "EUR",
        "GB": "GBP",
    }
    return currency_dict.get(country_code, "USD")

def get_subscription_benefits(subscription_type, currency):
    benefits = {
        "На тиждень": f"Переваги підписки на тиждень:\n- Повний доступ до всіх функцій\n- Пріоритетна підтримка\n\nЦіна: 10 {currency}",
        "На місяць": f"Переваги підписки на місяць:\n- Повний доступ до всіх функцій\n- Пріоритетна підтримка\n- Бонусні матеріали\n\nЦіна: 30 {currency}",
        "На рік": f"Переваги підписки на рік:\n- Повний доступ до всіх функцій\n- Пріоритетна підтримка\n- Бонусні матеріали\n- Спеціальні пропозиції\n\nЦіна: 300 {currency}",
        "Назавжди": f"Переваги підписки назавжди:\n- Повний доступ до всіх функцій\n- Пріоритетна підтримка\n- Бонусні матеріали\n- Спеціальні пропозиції\n- Пожиттєвий доступ\n\nЦіна: 1000 {currency}"
    }
    return benefits.get(subscription_type, "Невідомий тип підписки")

def search_profiles_by_criteria(user_profiles, city, min_age, max_age, search_preference):
    return [profile for uid, profile in user_profiles.items() if profile['city'] == city and min_age <= profile['age'] <= max_age and (search_preference == "Шукати всіх" or profile['gender'] == search_preference)]
