from fastapi import FastAPI, Request
from main import bot

app = FastAPI()

@app.post('/api/webhook')
async def webhook(request: Request):
    update = await request.json()
    await bot.process_update(update)
    return ''
