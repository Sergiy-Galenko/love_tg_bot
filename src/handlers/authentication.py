from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from .constants import START, MAIN_MENU_BUTTONS, NAME, PREMIUM, AGE_RANGE, ENTER_KEY

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

    if choice == "18+":
        await update.message.reply_text("Щоб отримати доступ, потрібен преміум.")
        return PREMIUM
    elif choice == "Знайомства":
        await update.message.reply_text("Введіть ваше ім'я:")
        return NAME
    elif choice == "Ввести унікальний ключ":
        await update.message.reply_text("Введіть унікальний ключ:")
        return ENTER_KEY

async def enter_key(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    key = update.message.text
    if key in premium_keys:
        duration = premium_keys[key]['duration']
        if 'profile' not in context.user_data:
            context.user_data['profile'] = {}
        context.user_data['profile']['premium'] = {
            'status': True,
            'duration': duration
        }
        del premium_keys[key]
        await update.message.reply_text(f"Преміум активовано на {duration}!")
        if duration == "На рік":
            await update.message.reply_text("Введіть мінімальний вік для пошуку:")
            return AGE_RANGE
    else:
        await update.message.reply_text("Унікальний ключ невірний. Спробуйте ще раз.")
    return START
