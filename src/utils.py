import random
import string
from sqlalchemy.ext.asyncio import AsyncSession

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

async def search_profiles_by_criteria(session: AsyncSession, city: str, min_age: int, max_age: int, search_preference: str, is_adult: bool, current_user_id: int):
    q = await session.execute(
        """SELECT user_id FROM user_profiles
           WHERE user_id != :uid
             AND LOWER(city) = :city
             AND age BETWEEN :min_age AND :max_age
             AND (:pref = 'шукати всіх' OR LOWER(gender) = :pref)
             AND is_adult = :is_adult
        """,
        {
            "uid": current_user_id,
            "city": city.lower(),
            "min_age": min_age,
            "max_age": max_age,
            "pref": search_preference.lower(),
            "is_adult": is_adult
        }
    )
    results = q.fetchall()
    return [r[0] for r in results]
