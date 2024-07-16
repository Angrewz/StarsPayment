import logging
from fastapi import FastAPI, Request
from main import bot

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.post('/api/webhook')
async def webhook(request: Request):
    update = await request.json()
    logging.info(f"Received update: {update}")
    await bot.process_update(update)
    return ''
