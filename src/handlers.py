from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from src.utils import (
    generate_unique_key, get_currency, get_subscription_benefits, 
    search_profiles_by_criteria
)
import random
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError

geolocator = Nominatim(user_agent="telegram_bot")

START, NAME, AGE, CITY, LOCATION, GENDER, SEARCH, CONFIRMATION, VIEW_PROFILES, SEARCH_PROFILES, PREMIUM, SUBSCRIPTION, GIFT, ENTER_KEY, AGE_RANGE, MAX_AGE, ADULT_NAME, ADULT_AGE, ADULT_CITY, ADULT_LOCATION, ADULT_GENDER, ADULT_SEARCH, ADULT_CONFIRMATION, ADULT_VIEW_PROFILES = range(24)

user_profiles = {}
current_profile_index = {}
premium_keys = {}

async def send_welcome_premium_message(update: Update, duration: str) -> None:
    await update.message.reply_text(
        f"Вітаємо з оформленням преміум підписки на {duration}!",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("Знайомства")],
                [KeyboardButton("18+")],
                [KeyboardButton("Ввести унікальний ключ")]
            ], 
            resize_keyboard=True
        )
    )
    try:
        await update.message.reply_sticker("CAACAgUAAxkBAAIKkWZ13fvfJF-qwg3ix6yvNxd7WERpAAKmAwAC6QrIA3mzkAhrhbH0NQQ")
    except Exception as e:
        print(f"Failed to send sticker: {e}")

async def send_gender_match_sticker(update: Update) -> None:
    try:
        await update.message.reply_sticker("CAACAgIAAxkBAAIKk2Z13glz9gcAATCnSDS6Jpq-lM0BhAACiQIAAladvQqhVs0CITIOPTUE")  # Замініть на правильний стікер
    except Exception as e:
        print(f"Failed to send gender match sticker: {e}")

async def send_special_gender_match_sticker(update: Update) -> None:
    try:
        await update.message.reply_sticker("CAACAgIAAxkBAAIKk2Z13glz9gcAATCnSDS6Jpq-lM0BhAACiQIAAladvQqhVs0CITIOPTUE")  # Замініть на правильний стікер
    except Exception as e:
        print(f"Failed to send special gender match sticker: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Виберіть опцію:",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("Знайомства")],
                [KeyboardButton("18+")],
                [KeyboardButton("Ввести унікальний ключ")]
            ], 
            resize_keyboard=True, one_time_keyboard=True
        )
    )
    return START

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    choice = update.message.text
    user_id = update.message.from_user.id

    if choice == "18+":
        user_profile = user_profiles.get(user_id)
        if user_profile and user_profile.get('premium', {}).get('status', False):
            await update.message.reply_text(
                "Введіть ваше ім'я для профілю 18+:",
                reply_markup=ReplyKeyboardMarkup(
                    [
                        [KeyboardButton(update.message.from_user.first_name)],
                        [KeyboardButton("Ввести інше ім'я")]
                    ], 
                    resize_keyboard=True, one_time_keyboard=True
                )
            )
            return ADULT_NAME
        else:
            await update.message.reply_text(
                "Щоб отримати доступ до цього розділу, вам потрібно оформити преміум-акаунт.",
                reply_markup=ReplyKeyboardMarkup(
                    [
                        [KeyboardButton("🔴 Купити преміум")],
                        [KeyboardButton("Назад")]
                    ], 
                    resize_keyboard=True
                )
            )
            return PREMIUM
    elif choice == "Знайомства":
        await update.message.reply_text(
            "Введіть ваше ім'я:",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [KeyboardButton(update.message.from_user.first_name)],
                    [KeyboardButton("Ввести інше ім'я")]
                ], 
                resize_keyboard=True, one_time_keyboard=True
            )
        )
        return NAME
    elif choice == "Ввести унікальний ключ":
        await update.message.reply_text("Введіть унікальний ключ:")
        return ENTER_KEY

async def enter_key(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    key = update.message.text
    user_id = update.message.from_user.id

    if key in premium_keys:
        duration = premium_keys[key]['duration']
        if user_id not in user_profiles:
            user_profiles[user_id] = {'premium': {}}
        user_profiles[user_id]['premium'] = {
            'status': True,
            'duration': duration
        }
        del premium_keys[key]
        await send_welcome_premium_message(update, duration)
        if duration == "На рік":
            await update.message.reply_text("Введіть мінімальний вік для пошуку:")
            return AGE_RANGE
    else:
        await update.message.reply_text("Унікальний ключ невірний. Спробуйте ще раз.")
    return START

async def premium_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    choice = update.message.text
    if choice == "Назад":
        await start(update, context)
        return START
    elif choice == "🔴 Купити преміум":
        await update.message.reply_text(
            "Виберіть тривалість підписки:",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [KeyboardButton("На тиждень")],
                    [KeyboardButton("На місяць")],
                    [KeyboardButton("На рік")],
                    [KeyboardButton("Назад")]
                ], 
                resize_keyboard=True
            )
        )
        return SUBSCRIPTION

async def subscription_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    choice = update.message.text
    if choice == "Назад":
        await premium_choice(update, context)
        return PREMIUM
    else:
        context.user_data['subscription'] = choice
        user_country = update.message.from_user.language_code
        currency = get_currency(user_country)
        await update.message.reply_text(
            get_subscription_benefits(choice, currency),
            reply_markup=ReplyKeyboardMarkup(
                [
                    [KeyboardButton("Купити для себе")],
                    [KeyboardButton("Купити в подарунок")],
                    [KeyboardButton("Назад")]
                ], 
                resize_keyboard=True
            )
        )
        return GIFT

async def gift_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    choice = update.message.text
    if choice == "Назад":
        user_country = update.message.from_user.language_code
        currency = get_currency(user_country)
        await update.message.reply_text(
            "Виберіть тривалість підписки:",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [KeyboardButton("На тиждень")],
                    [KeyboardButton("На місяць")],
                    [KeyboardButton("На рік")],
                    [KeyboardButton("Назад")]
                ], 
                resize_keyboard=True
            )
        )
        return SUBSCRIPTION
    elif choice == "Купити для себе":
        user_id = update.message.from_user.id
        duration = context.user_data['subscription']
        if user_id not in user_profiles:
            user_profiles[user_id] = {}
        user_profiles[user_id]['premium'] = {
            'status': True,
            'duration': duration
        }
        await send_welcome_premium_message(update, duration)
        if duration == "На рік":
            await update.message.reply_text("Введіть мінімальний вік для пошуку:")
            return AGE_RANGE
        return START
    elif choice == "Купити в подарунок":
        key = generate_unique_key()
        premium_keys[key] = {
            'duration': context.user_data['subscription']
        }
        await update.message.reply_text(f"Ваш унікальний ключ для подарунку: {key}", reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("Знайомства")],
                [KeyboardButton("18+")],
                [KeyboardButton("Ввести унікальний ключ")]
            ], 
                resize_keyboard=True
        ))
        return START

async def set_age_range(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        min_age = int(update.message.text)
        context.user_data['min_age'] = min_age
        await update.message.reply_text("Введіть максимальний вік для пошуку:")
        return MAX_AGE
    except ValueError:
        await update.message.reply_text("Будь ласка, введіть вік цифрами:")
        return AGE_RANGE

async def set_max_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        max_age = int(update.message.text)
        context.user_data['max_age'] = max_age
        await update.message.reply_text("Параметри пошуку збережено.")
        return START
    except ValueError:
        await update.message.reply_text("Будь ласка, введіть вік цифрами:")
        return MAX_AGE

async def set_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Введіть свій вік:")
    return AGE

async def set_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        context.user_data['age'] = int(update.message.text)
    except ValueError:
        await update.message.reply_text("Будь ласка, введіть вік цифрами:")
        return AGE
    await update.message.reply_text(
        "Будь ласка, поділіться вашим місцезнаходженням або введіть місто вручну.",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("Поділитися місцезнаходженням", request_location=True)],
                [KeyboardButton("Ввести місто вручну")]
            ], 
            resize_keyboard=True, one_time_keyboard=True
        )
    )
    return LOCATION

async def get_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.location:
        location = update.message.location
        try:
            user_location = geolocator.reverse(f"{location.latitude}, {location.longitude}", timeout=10)
            city = user_location.raw['address'].get('city', user_location.raw['address'].get('town', ''))
        except GeocoderServiceError as e:
            # Обхід проблеми з SSL-сертифікатом
            response = requests.get(
                f"https://nominatim.openstreetmap.org/reverse?lat={location.latitude}&lon={location.longitude}&format=json&addressdetails=1",
                verify=False
            )
            if response.status_code == 200:
                user_location = response.json()
                city = user_location.get('address', {}).get('city', user_location.get('address', {}).get('town', ''))
            else:
                await update.message.reply_text("Не вдалося визначити ваше місцезнаходження. Введіть своє місто вручну:")
                return CITY
        context.user_data['city'] = city
        await update.message.reply_text(
            f"Ваше місто: {city}.",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [KeyboardButton(f"Залишити місто ({city})")],
                    [KeyboardButton("Ввести вручну")]
                ], 
                resize_keyboard=True, one_time_keyboard=True
            )
        )
    else:
        await update.message.reply_text("Введіть своє місто:")
        return CITY
    return CITY

async def set_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "Ввести вручну":
        await update.message.reply_text("Введіть своє місто:")
        return CITY
    else:
        context.user_data['city'] = update.message.text
        await update.message.reply_text(
            "Виберіть свою стать:",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [KeyboardButton("Я хлопець 👦"), KeyboardButton("Я дівчина 👧")]
                ], 
                resize_keyboard=True, one_time_keyboard=True
            )
        )
        return GENDER

async def set_gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['gender'] = update.message.text
    await update.message.reply_text(
        "Кого ви хочете шукати?",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("Шукати хлопця 👦"), KeyboardButton("Шукати дівчину 👧")]
            ], 
            resize_keyboard=True, one_time_keyboard=True
        )
    )
    return SEARCH

async def process_search_preference(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    search_preference = update.message.text
    context.user_data['search_preference'] = search_preference
    profile = context.user_data

    await update.message.reply_text(
        f"Ваші дані:\nІм'я: {profile['name']}\nВік: {profile['age']}\nМісто: {profile['city']}\nСтать: {profile['gender']}\nШукає: {search_preference.lower()}\n\nВсе вірно?",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("Так")],
                [KeyboardButton("Ні")]
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
                    [KeyboardButton("Переглянути анкети")],
                    [KeyboardButton("Ні")]
                ], 
                resize_keyboard=True
            )
        )
        return VIEW_PROFILES
    else:
        await update.message.reply_text(
            "Ви повернулись до головного меню. Ваші дані збережені.",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [KeyboardButton("Знайомства")],
                    [KeyboardButton("18+")],
                    [KeyboardButton("Ввести унікальний ключ")]
                ], 
                resize_keyboard=True
            )
        )
        return START

async def view_profiles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    user_data = user_profiles.get(user_id)
    
    if not user_data:
        await update.message.reply_text("Спочатку створіть акаунт.")
        return ConversationHandler.END

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

    profiles = [profile for uid, profile in user_profiles.items() if uid != user_id and profile['city'] == city and profile.get('is_adult', False) == is_adult and min_age <= profile['age'] <= max_age and (search_preference == "Шукати всіх" or profile['gender'] == search_preference)]

    if profiles:
        random.shuffle(profiles)
        current_profile_index[user_id] = profiles
        await show_next_profile(update, context)
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
        if user_profile['gender'] == next_profile['gender']:
            await send_special_gender_match_sticker(update)
        else:
            await send_gender_match_sticker(update)

    await update.message.reply_text(
        f"Ім'я: {next_profile['name']}\nВік: {next_profile['age']}\nМісто: {next_profile['city']}\n",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("Наступний")]
            ], 
            resize_keyboard=True
        )
    )
    return VIEW_PROFILES

async def search_profiles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Введіть місто для пошуку:")
    return SEARCH_PROFILES

async def process_search_profiles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    city = update.message.text
    user_id = update.message.from_user.id
    user_data = user_profiles.get(user_id)

    if not user_data:
        await update.message.reply_text("Спочатку створіть акаунт.")
        return ConversationHandler.END

    user_age = user_data.get('age')
    min_age = user_age - 3
    max_age = user_age + 3
    search_preference = user_data.get('search_preference')
    is_adult = user_data.get('is_adult', False)

    matching_profiles = search_profiles_by_criteria(user_profiles, city, min_age, max_age, search_preference, is_adult)

    if matching_profiles:
        response = "Знайдені анкети:\n\n"
        for profile in matching_profiles:
            response += f"Ім'я: {profile['name']}\nВік: {profile['age']}\nМісто: {profile['city']}\n\n"
    else:
        response = "Не знайдено анкет, що відповідають вашим критеріям."

    await update.message.reply_text(response)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Скасовано.")
    return ConversationHandler.END
