from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
import random

# Становища для розмови
START, NAME, AGE, CITY, CONFIRMATION, SEARCH_PROFILES, EDIT_PROFILE, VIEW_PROFILES, PREMIUM = range(9)

# Зберігання даних користувачів у пам'яті
user_profiles = {}
current_profile_index = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        f"Вітаю, {user.first_name}! Виберіть опцію:",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("Знайомства")],
                [KeyboardButton("18+")]
            ], 
            resize_keyboard=True
        )
    )
    return START

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    choice = update.message.text
    if choice == "18+":
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
        user = update.message.from_user
        await update.message.reply_text(
            "Введіть своє ім'я або оберіть запропоноване:",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [KeyboardButton(user.first_name)],
                    [KeyboardButton("Ввести інше ім'я")]
                ], 
                resize_keyboard=True, one_time_keyboard=True
            )
        )
        return NAME

async def premium_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    choice = update.message.text
    if choice == "Назад":
        await start(update, context)
        return START
    elif choice == "🔴 Купити преміум":
        await update.message.reply_text("Функція оформлення преміум-акаунту ще не реалізована.")
        return PREMIUM

async def set_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "Ввести інше ім'я":
        await update.message.reply_text("Введіть своє ім'я:")
        return NAME
    else:
        context.user_data['name'] = update.message.text
        await update.message.reply_text("Введіть свій вік:")
        return AGE

async def set_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        context.user_data['age'] = int(update.message.text)
    except ValueError:
        await update.message.reply_text("Будь ласка, введіть вік цифрами:")
        return AGE
    await update.message.reply_text("Введіть своє місто:")
    return CITY

async def set_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['city'] = update.message.text
    profile = context.user_data
    await update.message.reply_text(
        f"Ваші дані:\nІм'я: {profile['name']}\nВік: {profile['age']}\nМісто: {profile['city']}\n\nВсе вірно?",
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
            "Що ви хочете відредагувати?",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [KeyboardButton("Ім'я")],
                    [KeyboardButton("Вік")],
                    [KeyboardButton("Місто")]
                ], 
                resize_keyboard=True
            )
        )
        return EDIT_PROFILE

async def edit_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "Ім'я":
        user = update.message.from_user
        await update.message.reply_text(
            "Введіть своє нове ім'я або оберіть запропоноване:",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [KeyboardButton(user.first_name)],
                    [KeyboardButton("Ввести інше ім'я")]
                ], 
                resize_keyboard=True, one_time_keyboard=True
            )
        )
        return NAME
    elif update.message.text == "Вік":
        await update.message.reply_text("Введіть свій новий вік:")
        return AGE
    elif update.message.text == "Місто":
        await update.message.reply_text("Введіть своє нове місто:")
        return CITY

async def view_profiles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    user_data = user_profiles.get(user_id)
    
    if not user_data:
        await update.message.reply_text("Спочатку створіть акаунт.")
        return ConversationHandler.END

    city = user_data.get('city')
    age = user_data.get('age')

    profiles = [profile for uid, profile in user_profiles.items() if uid != user_id and profile['city'] == city and age - 3 <= profile['age'] <= age + 3]

    if profiles:
        random.shuffle(profiles)
        current_profile_index[user_id] = profiles
        await show_next_profile(update, context)
    else:
        await update.message.reply_text("Немає анкет для перегляду.")
        return ConversationHandler.END
    return VIEW_PROFILES

async def show_next_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id

    if user_id not in current_profile_index or not current_profile_index[user_id]:
        await update.message.reply_text("Більше немає анкет для перегляду.")
        return ConversationHandler.END

    profiles = current_profile_index[user_id]
    next_profile = profiles.pop()
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

    matching_profiles = [profile for uid, profile in user_profiles.items() if uid != user_id and profile['city'] == city and min_age <= profile['age'] <= max_age]

    if matching_profiles:
        response = "Знайдені анкети:\n\n"
        for profile in matching_profiles:
            response += f"Ім'я: {profile['name']}\nВік: {profile['age']}\nМісто: {profile['city']}\n\n"
    else:
        response = "Не знайдено анкет, що відповідають вашим критеріям."

    await update.message.reply_text(response)
    return ConversationHandler.END
