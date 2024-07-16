import logging
from fastapi import FastAPI, Request
from main import bot

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.post('/api/webhook')
async def webhook(request: Request):
    logging.info("Webhook received")
    update = await request.json()
    logging.info(f"Update: {update}")
    await bot.initialize()  # Инициализируем объект Application перед использованием
    await bot.process_update(update)
    return ''

@app.get('/api/webhook')
async def webhook_status():
    return {"status": "Webhook is active"}
