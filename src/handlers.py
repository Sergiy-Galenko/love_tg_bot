from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
import random
import string

# Становища для розмови
START, NAME, AGE, CITY, CONFIRMATION, SEARCH_PROFILES, EDIT_PROFILE, VIEW_PROFILES, PREMIUM, SUBSCRIPTION, GIFT, ENTER_KEY = range(12)

# Зберігання даних користувачів у пам'яті
user_profiles = {}
current_profile_index = {}
premium_keys = {}

def generate_unique_key(length=12):
    """Generate a unique key for gifting premium subscription."""
    characters = string.ascii_letters + string.digits
    key = ''.join(random.choice(characters) for i in range(length))
    return key

def get_currency(country_code):
    """Return the currency based on the country code."""
    currency_dict = {
        "US": "USD",
        "UA": "UAH",
        "EU": "EUR",
        "GB": "GBP",
        # Додайте інші країни за потреби
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        f"Вітаю, {user.first_name}! Виберіть опцію:",
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
        await update.message.reply_text(f"Ваш преміум-акаунт активовано на {duration}!", reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("Знайомства")],
                [KeyboardButton("18+")],
                [KeyboardButton("Ввести унікальний ключ")]
            ], 
            resize_keyboard=True
        ))
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
                    [KeyboardButton("Назавжди")],
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
        user_country = update.message.from_user.language_code  # Приклад отримання коду країни
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
                    [KeyboardButton("Назавжди")],
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
        await update.message.reply_text(f"Ваш преміум-акаунт активовано на {duration}!", reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("Знайомства")],
                [KeyboardButton("18+")],
                [KeyboardButton("Ввести унікальний ключ")]
            ], 
            resize_keyboard=True
        ))
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
