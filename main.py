from telegram import Update, LabeledPrice
from telegram.ext import Application, CommandHandler, MessageHandler, PreCheckoutQueryHandler, CallbackContext, filters
import os
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv('YOUR_BOT_TOKEN')
PAYMENT_PROVIDER_TOKEN = 'YOUR_PAYMENT_PROVIDER_TOKEN'

# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> None:
    logging.info("Start command received")
    await update.message.reply_text("Привет! Введи свой вопрос, и я попрошу оплату в 1 ⭐️ перед ответом.")

# Обработчик получения сообщений (вопросов) от пользователей
async def handle_question(update: Update, context: CallbackContext) -> None:
    logging.info(f"Question received: {update.message.text}")
    chat_id = update.message.chat_id
    context.user_data['question'] = update.message.text
    title = "Оплата за ответ"
    description = "Ответ в обработке. Закончу сразу после оплаты."
    payload = "Custom-Payload"
    currency = "XTR"
    price = 1
    prices = [LabeledPrice("Оплата ответа на важнейший вопрос", price)]

    await context.bot.send_invoice(chat_id, title, description, payload, PAYMENT_PROVIDER_TOKEN, currency, prices)
    logging.info("Invoice sent")

# Обработчик предварительной проверки оплаты
async def precheckout_callback(update: Update, context: CallbackContext) -> None:
    logging.info("Precheckout received")
    query = update.pre_checkout_query
    if query.invoice_payload != 'Custom-Payload':
        await query.answer(ok=False, error_message="Что-то пошло не так...")
    else:
        await query.answer(ok=True)

# Обработчик успешной оплаты
async def successful_payment_callback(update: Update, context: CallbackContext) -> None:
    logging.info("Successful payment received")
    question = context.user_data.get('question', '')
    response = f"{question} - хороший вопрос, но я не знаю на него ответ. Зато желаю тебе всех благ. Добро возвращается! Смайлик"
    await update.message.reply_text(response)

async def set_webhook(application: Application):
    webhook_url = f"https://stars-payment.vercel.app/api/webhook"
    logging.info(f"Setting webhook to: {webhook_url}")
    await application.bot.set_webhook(webhook_url)

def create_application() -> Application:
    logging.info("Starting bot")
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question))
    application.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))

    return application

# Создаем приложение и устанавливаем вебхук
bot = create_application()
asyncio.run(set_webhook(bot))
