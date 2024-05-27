from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from src.handlers import (
    start, create_account, set_name, set_age, set_city,
    confirm_data, edit_profile, view_profiles, search_profiles, process_search_profiles,
    NAME, AGE, CITY, CONFIRMATION, SEARCH_PROFILES, EDIT_PROFILE
)

def main() -> None:
    application = Application.builder().token("7105850725:AAFItkfDHDVM4RNPEd0Hcgsts_3dMRiaJKo").build()
    
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^Створити акаунт$'), create_account)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_age)],
            CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_city)],
            CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_data)],
            EDIT_PROFILE: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_profile)],
            SEARCH_PROFILES: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_search_profiles)],
        },
        fallbacks=[CommandHandler('start', start)]
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.Regex('^Переглянути анкети$'), view_profiles))
    application.add_handler(MessageHandler(filters.Regex('^Пошук$'), search_profiles))

    application.run_polling()

if __name__ == '__main__':
    main()
