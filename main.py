from telegram import Update, LabeledPrice
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    PreCheckoutQueryHandler,
    CallbackContext,
    filters,
)
import os

# Замените на ваш токен бота и токен провайдера платежей
BOT_TOKEN = os.environ['YOUR_BOT_TOKEN']
PAYMENT_PROVIDER_TOKEN = 'YOUR_PAYMENT_PROVIDER_TOKEN'

# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Привет! Введи свой вопрос, и я попрошу оплату в 1 ⭐️ перед ответом.")

# Обработчик получения сообщений (вопросов) от пользователей
async def handle_question(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    context.user_data['question'] = update.message.text
    title = "Оплата за ответ"
    description = "Ответ в обработке. Закончу сразу после оплаты."
    payload = "Custom-Payload"
    currency = "XTR"  # Используйте XTR для "Звёзд"
    price = 1  # Установите цену в минимальных единицах "Звёзд" (1 Звезда = 100 единиц)
    prices = [LabeledPrice("Оплата ответа на важнейший вопрос", price)]

    # Отправка инвойса пользователю
    await context.bot.send_invoice(chat_id, title, description, payload, PAYMENT_PROVIDER_TOKEN, currency, prices)

# Обработчик предварительной проверки оплаты
async def precheckout_callback(update: Update, context: CallbackContext) -> None:
    query = update.pre_checkout_query
    if query.invoice_payload != 'Custom-Payload':
        await query.answer(ok=False, error_message="Что-то пошло не так...")
    else:
        await query.answer(ok=True)

# Обработчик успешной оплаты
async def successful_payment_callback(update: Update, context: CallbackContext) -> None:
    question = context.user_data.get('question', '')
    response = f"{question} - хороший вопрос, но я не знаю на него ответ. Зато желаю тебе всех благ. Добро возвращается! Смайлик"
    await update.message.reply_text(response)

def main() -> None:
    # Создание и запуск приложения
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question))
    application.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))

    # Запуск приложения
    application.run_polling()

if __name__ == '__main__':
    main()