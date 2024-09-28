from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from .constants import SEARCH, CONFIRMATION, VIEW_PROFILES, SEARCH_PROFILES, START, MAIN_MENU_BUTTONS, AGE_RANGE, MAX_AGE
from .utils import send_gender_match_sticker
from src.utils import search_profiles_by_criteria
import random

user_profiles = {}
current_profile_index = {}

async def process_search_preference(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    search_preference = update.message.text
    context.user_data['search_preference'] = search_preference
    profile = context.user_data

    if profile.get('photo'):
        with open(profile['photo'], 'rb') as photo:
            await update.message.reply_photo(photo)

    await update.message.reply_text(
        f"Ваші дані:\nІм'я: {profile['name']}\nВік: {profile['age']}\nМісто: {profile['city']}\nСтать: {profile['gender']}\nХобі: {profile.get('hobby', 'Не вказано')}\nШукає: {search_preference.lower()}\n\nВсе вірно?",
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
        context.user_data['username'] = update.message.from_user.username
        user_profiles[user_id] = context.user_data

        await update.message.reply_text(
            "Ваш акаунт створено! Хочете переглянути анкети інших людей?",
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
            "Ви повернулись до головного меню. Ваші дані збережені.",
            reply_markup=ReplyKeyboardMarkup(
                MAIN_MENU_BUTTONS,
                resize_keyboard=True
            )
        )
        return START

async def view_profiles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    user_data = user_profiles.get(user_id)

    if not user_data:
        await update.message.reply_text("Спочатку створіть акаунт.")
        return START

    city = user_data.get('city')
    age = user_data.get('age')
    search_preference = user_data.get('search_preference')
    is_adult = user_data.get('is_adult', False)

    if user_data.get('premium', {}).get('status', False) and user_data['premium'].get('duration') == "На рік":
        min_age = user_data.get('min_age', age - 3)
        max_age = user_data.get('max_age', age + 3)
    else:
        min_age = age - 3
        max_age = age + 3

    profiles = [
        profile for uid, profile in user_profiles.items()
        if uid != user_id and
        profile['city'].lower() == city.lower() and
        min_age <= profile['age'] <= max_age and
        (search_preference == "Шукати всіх" or profile['gender'] == search_preference) and
        profile.get('is_adult', False) == is_adult
    ]

    if profiles:
        random.shuffle(profiles)
        current_profile_index[user_id] = profiles
        await show_next_profile(update, context)
        return VIEW_PROFILES
    else:
        await update.message.reply_text("Немає анкет для перегляду.")
        return VIEW_PROFILES

async def show_next_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id

    if user_id not in current_profile_index or not current_profile_index[user_id]:
        await update.message.reply_text("Більше немає анкет для перегляду.")
        return VIEW_PROFILES

    profiles = current_profile_index[user_id]
    next_profile = profiles.pop()

    user_profile = user_profiles[user_id]
    if user_profile.get('premium', {}).get('status', False):
        await send_gender_match_sticker(update)

    if next_profile.get('photo'):
        with open(next_profile['photo'], 'rb') as photo:
            await update.message.reply_photo(photo)
    await update.message.reply_text(
        f"Ім'я: {next_profile['name']}\nВік: {next_profile['age']}\nМісто: {next_profile['city']}\nХобі: {next_profile.get('hobby', 'Не вказано')}\n",
        reply_markup=ReplyKeyboardMarkup(
            [
                ["Наступний"]
            ],
            resize_keyboard=True
        )
    )
    return VIEW_PROFILES

async def process_search_profiles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    search_city = update.message.text
    user_id = update.message.from_user.id
    user_data = user_profiles.get(user_id)

    if not user_data:
        await update.message.reply_text("Спочатку створіть акаунт.")
        return START

    search_preference = user_data.get('search_preference')
    age = user_data.get('age')
    is_adult = user_data.get('is_adult', False)

    if user_data.get('premium', {}).get('status', False) and user_data['premium'].get('duration') == "На рік":
        min_age = user_data.get('min_age', age - 3)
        max_age = user_data.get('max_age', age + 3)
    else:
        min_age = age - 3
        max_age = age + 3

    matching_profiles = search_profiles_by_criteria(user_profiles, search_city, min_age, max_age, search_preference, is_adult)

    if matching_profiles:
        response = "Знайдені анкети:\n\n"
        for profile in matching_profiles:
            response += f"Ім'я: {profile['name']}\nВік: {profile['age']}\nМісто: {profile['city']}\nХобі: {profile.get('hobby', 'Не вказано')}\n\n"
    else:
        response = "Не знайдено анкет, що відповідають вашим критеріям."

    await update.message.reply_text(response)
    return START
