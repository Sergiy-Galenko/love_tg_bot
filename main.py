import os
import asyncio
import nest_asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from src.handlers import (
    start, handle_choice, enter_key, premium_choice, subscription_choice,
    gift_choice, set_name, set_age, set_city, get_location, set_gender,
    process_search_preference, confirm_data, view_profiles, show_next_profile,
    set_hobby, set_photo, cancel,
    START, NAME, AGE, CITY, LOCATION, GENDER, SEARCH, CONFIRMATION, VIEW_PROFILES,
    PREMIUM, SUBSCRIPTION, GIFT, ENTER_KEY, AGE_RANGE, MAX_AGE, HOBBY, PHOTO
)
from src.database import engine, Base

nest_asyncio.apply()  # Дозволяє повторно використовувати вже існуючий цикл подій

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if not token:
        print("Будь ласка, встановіть TELEGRAM_BOT_TOKEN.")
        return

    await init_db()

    application = Application.builder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_choice)],
            ENTER_KEY: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_key)],
            PREMIUM: [MessageHandler(filters.TEXT & ~filters.COMMAND, premium_choice)],
            SUBSCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, subscription_choice)],
            GIFT: [MessageHandler(filters.TEXT & ~filters.COMMAND, gift_choice)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_age)],
            LOCATION: [
                MessageHandler(filters.LOCATION, get_location),
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_location)
            ],
            CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_city)],
            GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_gender)],
            HOBBY: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_hobby)],
            PHOTO: [
                MessageHandler(filters.PHOTO, set_photo),
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_photo)
            ],
            SEARCH: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_search_preference)],
            CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_data)],
            VIEW_PROFILES: [MessageHandler(filters.TEXT & ~filters.COMMAND, show_next_profile)],
            AGE_RANGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_age)],
            MAX_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_age)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)

    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
