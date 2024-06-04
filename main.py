from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from src.handlers import (
    start, handle_choice, premium_choice, set_name, set_age, set_city,
    confirm_data, edit_profile, view_profiles, search_profiles, process_search_profiles, show_next_profile,
    START, NAME, AGE, CITY, CONFIRMATION, SEARCH_PROFILES, EDIT_PROFILE, VIEW_PROFILES, PREMIUM
)

def main() -> None:
    application = Application.builder().token("7105850725:AAFItkfDHDVM4RNPEd0Hcgsts_3dMRiaJKo").build()  # Замініть на ваш правильний токен
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_choice)],
            PREMIUM: [MessageHandler(filters.TEXT & ~filters.COMMAND, premium_choice)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_age)],
            CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_city)],
            CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_data)],
            EDIT_PROFILE: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_profile)],
            VIEW_PROFILES: [MessageHandler(filters.Regex('^Наступний$'), show_next_profile)],
            SEARCH_PROFILES: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_search_profiles)],
        },
        fallbacks=[CommandHandler('start', start)]
    )

    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.Regex('^Переглянути анкети$'), view_profiles))
    application.add_handler(MessageHandler(filters.Regex('^Пошук$'), search_profiles))

    application.run_polling()

if __name__ == '__main__':
    main()
