from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from .constants import SEARCH, CONFIRMATION, VIEW_PROFILES, START, MAIN_MENU_BUTTONS
from src.models import UserProfile
from src.database import SessionLocal
from src.utils import search_profiles_by_criteria

async def process_search_preference(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    raw_choice = update.message.text
    # Нормалізуємо вибір користувача
    if raw_choice == "Шукати дівчину 👧":
        context.user_data['search_preference'] = 'female'
    elif raw_choice == "Шукати хлопця 👦":
        context.user_data['search_preference'] = 'male'
    elif raw_choice == "Шукати всіх":
        context.user_data['search_preference'] = 'all'
    else:
        context.user_data['search_preference'] = 'all'

    profile = context.user_data
    search_str = "дівчину" if profile['search_preference'] == 'female' else "хлопця" if profile['search_preference'] == 'male' else "всіх"

    if profile.get('photo'):
        with open(profile['photo'], 'rb') as photo:
            await update.message.reply_photo(photo)

    await update.message.reply_text(
        f"Ваші дані:\n"
        f"Ім'я: {profile.get('name', 'Не вказано')}\n"
        f"Вік: {profile.get('age', 'Не вказано')}\n"
        f"Місто: {profile.get('city', 'Не вказано')}\n"
        f"Стать: {profile.get('gender', 'Не вказано')}\n"
        f"Хобі: {profile.get('hobby', 'Не вказано')}\n"
        f"Шукає: {search_str}\n\n"
        "Все вірно?",
        reply_markup=ReplyKeyboardMarkup(
            [
                ["Так"],
                ["Ні"]
            ],
            resize_keyboard=True
        )
    )
    return CONFIRMATION


async def confirm_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "Так":
        user_id = update.message.from_user.id
        profile_data = context.user_data
        premium_info = profile_data.get('premium', {})

        async with SessionLocal() as session:
            user_profile = UserProfile(
                user_id=user_id,  # Тут уже user_id великий int, тепер в БД BigInteger
                username=update.message.from_user.username,
                name=profile_data['name'],
                age=profile_data['age'],
                city=profile_data['city'].lower(),  # Переконайтеся, що місто нижнього регістру
                gender=profile_data['gender'],       # 'male', 'female' або інше
                hobby=profile_data.get('hobby'),
                search_preference=profile_data['search_preference'],  # 'male', 'female' або 'all'
                photo=profile_data.get('photo'),
                is_adult=False,
                premium_status=premium_info.get('status', False),
                premium_duration=premium_info.get('duration'),
                min_age=profile_data.get('min_age'),
                max_age=profile_data.get('max_age')
            )
            session.add(user_profile)
            await session.commit()

        await update.message.reply_text(
            "Ваш акаунт створено! Переглянути анкети інших?",
            reply_markup=ReplyKeyboardMarkup(
                [
                    ["Переглянути анкети"],
                    ["Ні"]
                ],
                resize_keyboard=True
            )
        )
        return VIEW_PROFILES
    else:
        await update.message.reply_text(
            "Ви повернулись до головного меню.",
            reply_markup=ReplyKeyboardMarkup(MAIN_MENU_BUTTONS, resize_keyboard=True)
        )
        return START

async def view_profiles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    async with SessionLocal() as session:
        user_data = await session.scalar(
            session.select(UserProfile).where(UserProfile.user_id == user_id)
        )
        if not user_data:
            await update.message.reply_text("Спочатку створіть акаунт.")
            return START

        city = user_data.city.lower()
        age = user_data.age
        search_preference = user_data.search_preference  # 'male', 'female' або 'all'
        is_adult = user_data.is_adult

        if user_data.premium_status and user_data.premium_duration == "На рік":
            min_age = user_data.min_age if user_data.min_age else age - 3
            max_age = user_data.max_age if user_data.max_age else age + 3
        else:
            min_age = age - 3
            max_age = age + 3

        # Шукаємо відповідні профілі
        matching_ids = await search_profiles_by_criteria(session, city, min_age, max_age, search_preference, is_adult, user_id)
        if matching_ids:
            context.user_data['profiles'] = matching_ids
            await show_next_profile(update, context)
            return VIEW_PROFILES
        else:
            await update.message.reply_text("Немає анкет для перегляду.")
            return VIEW_PROFILES

async def show_next_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    profiles = context.user_data.get('profiles', [])

    if not profiles:
        await update.message.reply_text("Більше немає анкет.")
        return VIEW_PROFILES

    target_user_id = profiles.pop()
    async with SessionLocal() as session:
        target_profile = await session.scalar(
            session.select(UserProfile).where(UserProfile.user_id == target_user_id)
        )

        if not target_profile:
            await update.message.reply_text("Профіль недоступний.")
            return VIEW_PROFILES

        if target_profile.photo:
            with open(target_profile.photo, 'rb') as photo:
                await update.message.reply_photo(photo)

        # Показуємо дані знайденого профілю
        await update.message.reply_text(
            f"Ім'я: {target_profile.name}\n"
            f"Вік: {target_profile.age}\n"
            f"Місто: {target_profile.city}\n"
            f"Хобі: {target_profile.hobby if target_profile.hobby else 'Не вказано'}",
            reply_markup=ReplyKeyboardMarkup(
                [
                    ["Наступний"]
                ],
                resize_keyboard=True
            )
        )
    return VIEW_PROFILES
