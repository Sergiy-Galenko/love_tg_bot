from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from src.handlers import (
    start, handle_choice, enter_key, premium_choice, subscription_choice, 
    gift_choice, set_name, set_age, set_city, get_location, set_gender, 
    process_search_preference, confirm_data, view_profiles, show_next_profile,
    search_profiles, process_search_profiles, cancel, set_age_range, set_max_age, set_hobby,
    START, NAME, AGE, CITY, LOCATION, GENDER, SEARCH, CONFIRMATION, VIEW_PROFILES, SEARCH_PROFILES, PREMIUM, SUBSCRIPTION, GIFT, ENTER_KEY, AGE_RANGE, MAX_AGE, ADULT_NAME, ADULT_AGE, ADULT_CITY, ADULT_LOCATION, ADULT_GENDER, ADULT_SEARCH, ADULT_CONFIRMATION, ADULT_VIEW_PROFILES, HOBBY
)

def main() -> None:
    application = Application.builder().token("7105850725:AAFItkfDHDVM4RNPEd0Hcgsts_3dMRiaJKo").build()

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
            LOCATION: [MessageHandler(filters.LOCATION, get_location), MessageHandler(filters.TEXT & ~filters.COMMAND, get_location)],
            CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_city)],
            GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_gender)],
            HOBBY: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_hobby)],
            SEARCH: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_search_preference)],
            CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_data)],
            VIEW_PROFILES: [MessageHandler(filters.TEXT & ~filters.COMMAND, show_next_profile)],
            SEARCH_PROFILES: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_search_profiles)],
            AGE_RANGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_age_range)],
            MAX_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_max_age)],
            ADULT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_name)],
            ADULT_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_age)],
            ADULT_LOCATION: [MessageHandler(filters.LOCATION, get_location), MessageHandler(filters.TEXT & ~filters.COMMAND, get_location)],
            ADULT_CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_city)],
            ADULT_GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_gender)],
            ADULT_SEARCH: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_search_preference)],
            ADULT_CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_data)],
            ADULT_VIEW_PROFILES: [MessageHandler(filters.TEXT & ~filters.COMMAND, show_next_profile)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()
