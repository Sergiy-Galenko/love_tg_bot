from telegram import KeyboardButton

START, NAME, AGE, CITY, LOCATION, GENDER, SEARCH, CONFIRMATION, VIEW_PROFILES, SEARCH_PROFILES, PREMIUM, SUBSCRIPTION, GIFT, ENTER_KEY, AGE_RANGE, MAX_AGE, ADULT_NAME, ADULT_AGE, ADULT_CITY, ADULT_LOCATION, ADULT_GENDER, ADULT_SEARCH, ADULT_CONFIRMATION, ADULT_VIEW_PROFILES, HOBBY, PHOTO = range(26)

MAIN_MENU_BUTTONS = [
    [KeyboardButton("Знайомства")],
    [KeyboardButton("18+")],
    [KeyboardButton("Ввести унікальний ключ")]
]
