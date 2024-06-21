from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Функція для обробки стартової команди
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привіт! Надішліть мені стікер, і я поверну його ID.')

# Функція для обробки стікерів
async def sticker_handler(update: Update, context: CallbackContext) -> None:
    sticker_id = update.message.sticker.file_id
    await update.message.reply_text(f'ID цього стікера: {sticker_id}')

def main() -> None:
    # Введіть свій токен бота тут
    token = '7105850725:AAFItkfDHDVM4RNPEd0Hcgsts_3dMRiaJKo'

    # Створення аплікації
    application = Application.builder().token(token).build()

    # Реєстрація обробників команд та повідомлень
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Sticker.ALL, sticker_handler))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
