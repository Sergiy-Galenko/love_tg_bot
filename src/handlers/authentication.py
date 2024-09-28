
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from .constants import START, MAIN_MENU_BUTTONS,NAME, PREMIUM, AGE_RANGE, ENTER_KEY
from .premium import premium_choice
from .utils import send_welcome_premium_message
from src.utils import get_currency

premium_keys = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Виберіть опцію:",
        reply_markup=ReplyKeyboardMarkup(
            MAIN_MENU_BUTTONS,
            resize_keyboard=True, one_time_keyboard=True
        )
    )
    return START

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    choice = update.message.text
    user_id = update.message.from_user.id

    if choice == "18+":
        user_profile = context.user_data.get('profile')
        if user_profile and user_profile.get('premium', {}).get('status', False):
            await update.message.reply_text(
                "Введіть ваше ім'я для профілю 18+:",
                reply_markup=ReplyKeyboardMarkup(
                    [
                        [update.message.from_user.first_name],
                        ["Ввести інше ім'я"]
                    ],
                    resize_keyboard=True, one_time_keyboard=True
                )
            )
            return START  # Змінити на відповідний стан для ADULT_NAME
        else:
            await update.message.reply_text(
                "Щоб отримати доступ до цього розділу, вам потрібно оформити преміум-акаунт.",
                reply_markup=ReplyKeyboardMarkup(
                    [
                        ["🔴 Купити преміум"],
                        ["Назад"]
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
                    [update.message.from_user.first_name],
                    ["Ввести інше ім'я"]
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
        if 'profile' not in context.user_data:
            context.user_data['profile'] = {'premium': {}}
        context.user_data['profile']['premium'] = {
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
