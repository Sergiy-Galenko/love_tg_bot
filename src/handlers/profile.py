from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from .constants import NAME, AGE, CITY, LOCATION, GENDER, HOBBY, PHOTO, SEARCH
from .utils import get_city_from_location, save_photo

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
                ["Ввести місто вручну"]
            ],
            resize_keyboard=True, one_time_keyboard=True
        )
    )
    return LOCATION

async def get_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.location:
        location = update.message.location
        city = await get_city_from_location(location)
        if city:
            context.user_data['city'] = city
            await update.message.reply_text(
                f"Ваше місто: {city}.",
                reply_markup=ReplyKeyboardMarkup(
                    [
                        [f"Залишити місто ({city})"],
                        ["Ввести вручну"]
                    ],
                    resize_keyboard=True, one_time_keyboard=True
                )
            )
            return CITY
        else:
            await update.message.reply_text("Не вдалося визначити ваше місто. Введіть своє місто вручну:")
            return CITY
    else:
        await update.message.reply_text("Введіть своє місто:")
        return CITY

async def set_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "Ввести вручну":
        await update.message.reply_text("Введіть своє місто:")
        return CITY
    elif update.message.text.startswith("Залишити місто ("):
        pass
    else:
        context.user_data['city'] = update.message.text
    await update.message.reply_text(
        "Виберіть свою стать:",
        reply_markup=ReplyKeyboardMarkup(
            [
                ["Я хлопець 👦", "Я дівчина 👧"]
            ],
            resize_keyboard=True, one_time_keyboard=True
        )
    )
    return GENDER

async def set_gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['gender'] = update.message.text
    await update.message.reply_text(
        "Завантажте ваше фото:",
        reply_markup=ReplyKeyboardMarkup(
            [
                ["Пропустити"]
            ],
            resize_keyboard=True, one_time_keyboard=True
        )
    )
    return PHOTO

async def set_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.photo:
        photo_file = await update.message.photo[-1].get_file()
        photo_path = await save_photo(photo_file, update.message.from_user.id)  # await тут, оскільки тепер використовуємо async
        context.user_data['photo'] = photo_path
        await update.message.reply_text("Ваше фото збережено.")
    else:
        context.user_data['photo'] = None
    await update.message.reply_text("Розкажіть про себе або вкажіть ваші хобі:")
    return HOBBY

async def set_hobby(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['hobby'] = update.message.text
    await update.message.reply_text(
        "Кого ви хочете шукати?",
        reply_markup=ReplyKeyboardMarkup(
            [
                ["Шукати хлопця 👦", "Шукати дівчину 👧"],
                ["Шукати всіх"]
            ],
            resize_keyboard=True, one_time_keyboard=True
        )
    )
    return SEARCH
