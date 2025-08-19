import logging
import datetime
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ======= CONFIG LANGSUNG =======
TOKEN = "8246154695:AAFFJRh3l_94cHqjyLzV9ncyld7OM76qoyU"  # Ganti dengan token bot kamu
GROUP_ID = -1003056662193                                    # Ganti dengan ID grup private
CHANNEL_ID = -1002782196938                                   # Ganti dengan ID channel umum

# ======= LOGGING =======
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ======= MESSAGE FORWARDING =======
async def forward_testi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if not msg:
        return

    text = msg.text or msg.caption or ""
    if "#profit" not in text:
        return  # hanya teruskan pesan dengan #profit

    if msg.text:
        await context.bot.send_message(
            CHANNEL_ID,
            f"{msg.text}"
        )
    elif msg.sticker:
        await context.bot.send_sticker(CHANNEL_ID, msg.sticker.file_id)
    elif msg.photo:
        photo_file = msg.photo[-1].file_id
        caption = msg.caption or ""
        await context.bot.send_photo(
            CHANNEL_ID,
            photo_file,
            caption=caption
        )
    elif msg.video:
        video_file = msg.video.file_id
        caption = msg.caption or ""
        await context.bot.send_video(
            CHANNEL_ID,
            video_file,
            caption=caption
        )
    elif msg.document:
        doc_file = msg.document.file_id
        caption = msg.caption or ""
        await context.bot.send_document(
            CHANNEL_ID,
            doc_file,
            caption=caption
        )

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

    # Handler untuk forward pesan dari grup private
    app.add_handler(MessageHandler(filters.Chat(GROUP_ID), forward_testi))

    # Scheduler greetings
    scheduler = AsyncIOScheduler()
    scheduler.add_job(lambda: asyncio.create_task(send_greeting(app)), 'cron', hour=7, minute=0)
    scheduler.add_job(lambda: asyncio.create_task(send_greeting(app)), 'cron', hour=12, minute=0)
    scheduler.add_job(lambda: asyncio.create_task(send_greeting(app)), 'cron', hour=0, minute=0)
    scheduler.start()
    logger.info("Scheduler started")

    # Jalankan bot
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

# ======= START BOT =======
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
