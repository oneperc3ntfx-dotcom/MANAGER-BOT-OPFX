import logging
import datetime
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# =================== CONFIG ===================
TOKEN = "8246154695:AAFFJRh3l_94cHqjyLzV9ncyld7OM76qoyU"  # Ganti dengan token bot kamu
GROUP_ID = -1003056662193                                    # Ganti dengan ID grup private
CHANNEL_ID = -1002782196938                                   # Ganti dengan ID channel umum

# =================== LOGGING ===================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# =================== FORWARD PESAN ===================
async def forward_testi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return

    text = msg.text or msg.caption or ""
    if "#profit" not in text:
        return  # Hanya lanjutkan jika ada #profit

    # Forward berdasarkan tipe pesan
    if msg.text:
        await context.bot.send_message(CHANNEL_ID, msg.text)
    elif msg.sticker:
        await context.bot.send_sticker(CHANNEL_ID, msg.sticker.file_id)
    elif msg.photo:
        await context.bot.send_photo(
            CHANNEL_ID, msg.photo[-1].file_id, caption=msg.caption or ""
        )
    elif msg.video:
        await context.bot.send_video(
            CHANNEL_ID, msg.video.file_id, caption=msg.caption or ""
        )
    elif msg.document:
        await context.bot.send_document(
            CHANNEL_ID, msg.document.file_id, caption=msg.caption or ""
        )

# =================== GREETINGS ===================
async def send_greeting(app):
    now = datetime.datetime.now()
    hour = now.hour
    text = ""

    if hour == 7:
        text = "Selamat pagi trader! Semoga hari ini penuh profit 😊"
    elif hour == 12:
        text = "Selamat siang, jangan lupa makan siang para trader 💪"
    elif hour == 0:
        text = "Waktunya istirahat, semoga mimpi indah dan profit hari ini 🌙"
    else:
        return

    await app.bot.send_message(GROUP_ID, text)
    await app.bot.send_message(CHANNEL_ID, text)

# =================== MAIN ===================
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Handler untuk forward pesan dari grup private
    app.add_handler(MessageHandler(filters.Chat(GROUP_ID), forward_testi))

    # Scheduler greetings
    scheduler = AsyncIOScheduler()
    scheduler.add_job(lambda: asyncio.create_task(send_greeting(app)), 'cron', hour=7, minute=0)
    scheduler.add_job(lambda: asyncio.create_task(send_greeting(app)), 'cron', hour=12, minute=0)
    scheduler.add_job(lambda: asyncio.create_task(send_greeting(app)), 'cron', hour=0, minute=0)
    scheduler.start()
    logger.info("Scheduler started")

    # Jalankan bot (v20+ style)
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
