from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError
import requests
import os

from .constants import PREMIUM_STICKER_ID, LOVE_STICKER_ID, MAIN_MENU_BUTTONS

geolocator = Nominatim(user_agent="telegram_bot")

async def send_welcome_premium_message(update: Update, duration: str) -> None:
    await update.message.reply_text(
        f"Вітаємо з оформленням преміум підписки на {duration}!",
        reply_markup=ReplyKeyboardMarkup(
            MAIN_MENU_BUTTONS,
            resize_keyboard=True
        )
    )
    try:
        await update.message.reply_sticker(PREMIUM_STICKER_ID)
    except Exception as e:
        print(f"Failed to send premium sticker: {e}")

async def send_gender_match_sticker(update: Update) -> None:
    try:
        await update.message.reply_sticker(LOVE_STICKER_ID)
    except Exception as e:
        print(f"Failed to send love sticker: {e}")

async def get_city_from_location(location) -> str:
    city = ''
    try:
        user_location = geolocator.reverse(f"{location.latitude}, {location.longitude}", timeout=10)
        if user_location and 'address' in user_location.raw:
            city = user_location.raw['address'].get('city', user_location.raw['address'].get('town', ''))
    except GeocoderServiceError:
        pass

    if not city:
        # Спробуємо через HTTP-запит
        response = requests.get(
            f"https://nominatim.openstreetmap.org/reverse?lat={location.latitude}&lon={location.longitude}&format=json&addressdetails=1",
            verify=False
        )
        if response.status_code == 200:
            user_location = response.json()
            city = user_location.get('address', {}).get('city', user_location.get('address', {}).get('town', ''))

    return city if city else None

async def save_photo(photo_file, user_id):
    photo_path = f"user_photos/{user_id}.jpg"
    os.makedirs(os.path.dirname(photo_path), exist_ok=True)
    await photo_file.download_to_drive(photo_path)
    return photo_path
