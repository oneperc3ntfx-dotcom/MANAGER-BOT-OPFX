from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CallbackContext, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import datetime

# ======= CONFIG =======
TOKEN = "8246154695:AAFFJRh3l_94cHqjyLzV9ncyld7OM76qoyU"
GROUP_ID = -1003056662193
CHANNEL_ID = "-1002782196938"  
# =====================

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ======= MESSAGE FORWARDING FUNCTION =======
def forward_testi(update: Update, context: CallbackContext):
    msg = update.message

    # TEKS
    if msg.text:
        context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=f"{msg.text}\n\n#profit"
        )
    
    # STIKER
    elif msg.sticker:
        context.bot.send_sticker(
            chat_id=CHANNEL_ID,
            sticker=msg.sticker.file_id
        )
    
    # FOTO
    elif msg.photo:
        photo_file = msg.photo[-1].file_id
        caption = msg.caption if msg.caption else ""
        context.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=photo_file,
            caption=f"{caption}\n\n#profit" if caption else "#profit"
        )
    
    # VIDEO
    elif msg.video:
        video_file = msg.video.file_id
        caption = msg.caption if msg.caption else ""
        context.bot.send_video(
            chat_id=CHANNEL_ID,
            video=video_file,
            caption=f"{caption}\n\n#profit" if caption else "#profit"
        )
    
    # DOKUMEN
    elif msg.document:
        doc_file = msg.document.file_id
        caption = msg.caption if msg.caption else ""
        context.bot.send_document(
            chat_id=CHANNEL_ID,
            document=doc_file,
            caption=f"{caption}\n\n#profit" if caption else "#profit"
        )

# ======= SCHEDULED GREETINGS =======
def send_greeting(context: CallbackContext):
    now = datetime.datetime.now()
    hour = now.hour

    # Pesan sesuai waktu
    if hour == 7:  # Selamat pagi
        text = "Selamat pagi trader! Semoga hari ini penuh profit 😊"
    elif hour == 12:  # Selamat siang
        text = "Selamat siang, jangan lupa makan siang para trader, biar ada tenaga untuk melawan market 💪"
    elif hour == 0:  # Selamat malam
        text = "Waktunya istirahat, semoga mimpi indah dan profit hari ini 🌙"
    else:
        return  # Skip jika bukan waktu yang diinginkan

    # Kirim ke grup private dan channel publik
    context.bot.send_message(chat_id=GROUP_ID, text=text)
    context.bot.send_message(chat_id=CHANNEL_ID, text=text)

# ======= MAIN =======
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Forwarding handler untuk semua pesan dari grup
    dp.add_handler(MessageHandler(Filters.chat(chat_id=GROUP_ID), forward_testi))

    # Scheduler untuk greetings
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: send_greeting(updater.bot), 'cron', hour=7, minute=0)
    scheduler.add_job(lambda: send_greeting(updater.bot), 'cron', hour=12, minute=0)
    scheduler.add_job(lambda: send_greeting(updater.bot), 'cron', hour=0, minute=0)
    scheduler.start()

    # Start bot
    updater.start_polling()
    logging.info("Bot started...")
    updater.idle()

if __name__ == "__main__":
    main()
