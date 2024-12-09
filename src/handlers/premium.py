from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from .constants import PREMIUM, SUBSCRIPTION, GIFT, START, MAIN_MENU_BUTTONS, AGE_RANGE
from src.utils import generate_unique_key, get_currency, get_subscription_benefits

premium_keys = {}

async def premium_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    choice = update.message.text
    if choice == "Назад":
        await update.message.reply_text(
            "Виберіть опцію:",
            reply_markup=ReplyKeyboardMarkup(
                MAIN_MENU_BUTTONS,
                resize_keyboard=True, one_time_keyboard=True
            )
        )
        return START
    elif choice == "🔴 Купити преміум":
        await update.message.reply_text(
            "Виберіть тривалість підписки:",
            reply_markup=ReplyKeyboardMarkup(
                [
                    ["На тиждень"],
                    ["На місяць"],
                    ["На рік"],
                    ["Назад"]
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
                    ["Купити для себе"],
                    ["Купити в подарунок"],
                    ["Назад"]
                ],
                resize_keyboard=True
            )
        )
        return GIFT

async def gift_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    choice = update.message.text
    if choice == "Назад":
        await subscription_choice(update, context)
        return SUBSCRIPTION
    elif choice == "Купити для себе":
        duration = context.user_data['subscription']
        if 'profile' not in context.user_data:
            context.user_data['profile'] = {}
        context.user_data['profile']['premium'] = {
            'status': True,
            'duration': duration
        }
        await update.message.reply_text(f"Преміум на {duration} активовано!")
        if duration == "На рік":
            await update.message.reply_text("Введіть мінімальний вік для пошуку:")
            return AGE_RANGE
        return START
    elif choice == "Купити в подарунок":
        key = generate_unique_key()
        premium_keys[key] = {
            'duration': context.user_data['subscription']
        }
        await update.message.reply_text(
            f"Ваш унікальний ключ для подарунку: {key}",
            reply_markup=ReplyKeyboardMarkup(
                MAIN_MENU_BUTTONS,
                resize_keyboard=True
            )
        )
        return START
