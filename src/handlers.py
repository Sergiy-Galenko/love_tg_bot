from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
import random

# Становища для розмови
NAME, AGE, CITY, CONFIRMATION, SEARCH_PROFILES, EDIT_PROFILE, VIEW_PROFILES = range(7)

# Зберігання профілів користувачів
user_profiles = {}

# Зберігання поточних переглядів профілів
current_profile_index = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    await update.message.reply_text(
        f"Вітаю, {user.first_name}! Виберіть опцію:",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("Створити акаунт")],
                [KeyboardButton("Переглянути анкети")],
                [KeyboardButton("Пошук")]
            ], 
            resize_keyboard=True
        )
    )

async def create_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        "Введіть своє ім'я:",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton(user.first_name)]
            ], 
            resize_keyboard=True, one_time_keyboard=True
        )
    )
    return NAME

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
        await update.message.reply_text("Введіть своє нове ім'я:")
        return NAME
    elif update.message.text == "Вік":
        await update.message.reply_text("Введіть свій новий вік:")
        return AGE
    elif update.message.text == "Місто":
        await update.message.reply_text("Введіть своє нове місто:")
        return CITY

async def view_profiles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    profiles = list(user_profiles.keys())
    if user_id in profiles:
        profiles.remove(user_id)

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
    next_profile_id = profiles.pop()
    profile = user_profiles[next_profile_id]
    await update.message.reply_text(
        f"Ім'я: {profile['name']}\nВік: {profile['age']}\nМісто: {profile['city']}\n",
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
    user_age = context.user_data.get('age')
    if not user_age:
        await update.message.reply_text("Спочатку створіть акаунт.")
        return ConversationHandler.END
    min_age = user_age - 3
    max_age = user_age + 3

    matching_profiles = [
        profile for uid, profile in user_profiles.items()
        if uid != user_id and profile['city'] == city and min_age <= profile['age'] <= max_age
    ]

    if matching_profiles:
        response = "Знайдені анкети:\n\n"
        for profile in matching_profiles:
            response += f"Ім'я: {profile['name']}\nВік: {profile['age']}\nМісто: {profile['city']}\n\n"
    else:
        response = "Не знайдено анкет, що відповідають вашим критеріям."

    await update.message.reply_text(response)
    return ConversationHandler.END
