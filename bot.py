import os
import logging
import datetime
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

# ======= LOAD ENV =======
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# ======= LOGGING =======
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ======= MESSAGE FORWARDING =======
async def forward_testi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if msg.text:
        await context.bot.send_message(CHANNEL_ID, f"{msg.text}\n\n#profit")
    elif msg.sticker:
        await context.bot.send_sticker(CHANNEL_ID, msg.sticker.file_id)
    elif msg.photo:
        photo_file = msg.photo[-1].file_id
        caption = msg.caption or ""
        await context.bot.send_photo(CHANNEL_ID, photo_file, caption=f"{caption}\n\n#profit" if caption else "#profit")
    elif msg.video:
        video_file = msg.video.file_id
        caption = msg.caption or ""
        await context.bot.send_video(CHANNEL_ID, video_file, caption=f"{caption}\n\n#profit" if caption else "#profit")
    elif msg.document:
        doc_file = msg.document.file_id
        caption = msg.caption or ""
        await context.bot.send_document(CHANNEL_ID, doc_file, caption=f"{caption}\n\n#profit" if caption else "#profit")

# ======= GREETINGS =======
async def send_greeting(app):
    now = datetime.datetime.now()
    hour = now.hour

    if hour == 7:
        text = "Selamat pagi trader! Semoga hari ini penuh profit 😊"
    elif hour == 12:
        text = "Selamat siang, jangan lupa makan siang para trader, biar ada tenaga untuk melawan market 💪"
    elif hour == 0:
        text = "Waktunya istirahat, semoga mimpi indah dan profit hari ini 🌙"
    else:
        return

    await app.bot.send_message(GROUP_ID, text)
    await app.bot.send_message(CHANNEL_ID, text)

# ======= MAIN =======
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Handler untuk forward semua pesan dari grup
    app.add_handler(MessageHandler(filters.Chat(GROUP_ID), forward_testi))

    # Scheduler greetings
    scheduler = AsyncIOScheduler()
    scheduler.add_job(lambda: asyncio.create_task(send_greeting(app)), 'cron', hour=7, minute=0)
    scheduler.add_job(lambda: asyncio.create_task(send_greeting(app)), 'cron', hour=12, minute=0)
    scheduler.add_job(lambda: asyncio.create_task(send_greeting(app)), 'cron', hour=0, minute=0)
    scheduler.start()

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
