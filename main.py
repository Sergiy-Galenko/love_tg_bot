from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from src.handlers import (
    start, handle_choice, enter_key, premium_choice, subscription_choice, 
    gift_choice, set_name, set_age, set_city, get_location, set_gender, 
    process_search_preference, confirm_data, view_profiles, show_next_profile,
    search_profiles, process_search_profiles, cancel,
    START, NAME, AGE, CITY, LOCATION, GENDER, SEARCH, CONFIRMATION, VIEW_PROFILES, SEARCH_PROFILES, PREMIUM, SUBSCRIPTION, GIFT, ENTER_KEY
)

def main() -> None:
    application = Application.builder().token("7105850725:AAFItkfDHDVM4RNPEd0Hcgsts_3dMRiaJKo").build()  # Замініть на ваш правильний токен

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
            CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_city)],
            LOCATION: [MessageHandler(filters.LOCATION | filters.TEXT & ~filters.COMMAND, get_location)],
            GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_gender)],
            SEARCH: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_search_preference)],
            CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_data)],
            VIEW_PROFILES: [MessageHandler(filters.Regex('^Наступний$'), show_next_profile)],
            SEARCH_PROFILES: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_search_profiles)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.Regex('^Переглянути анкети$'), view_profiles))
    application.add_handler(MessageHandler(filters.Regex('^Пошук$'), search_profiles))

    application.run_polling(stop_signals=None)

if __name__ == '__main__':
    main()