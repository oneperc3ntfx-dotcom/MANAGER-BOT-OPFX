import logging
import datetime
import asyncio
import pytz
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# =================== CONFIG ===================
TOKEN = "8246154695:AAFFJRh3l_94cHqjyLzV9ncyld7OM76qoyU"  # Ganti dengan token bot kamu
GROUP_ID = -1003056662193                                  # ID grup private
CHANNEL_ID = -1002782196938                                # ID channel umum

# =================== LOGGING ===================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
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
        return  # Hanya teruskan jika ada #profit

    # Ambil nama & username pengirim
    if msg.from_user:
        name = msg.from_user.full_name
        username = f" (@{msg.from_user.username})" if msg.from_user.username else ""
        sender = f"{name}{username}"
    else:
        sender = "Anonim"

    if msg.text:
        await context.bot.send_message(CHANNEL_ID, f"Dari {sender}:\n{text}")
    elif msg.sticker:
        await context.bot.send_message(CHANNEL_ID, f"Dari {sender}:")
        await context.bot.send_sticker(CHANNEL_ID, msg.sticker.file_id)
    elif msg.photo:
        await context.bot.send_photo(
            CHANNEL_ID,
            msg.photo[-1].file_id,
            caption=f"Dari {sender}:\n{msg.caption or ''}"
        )
    elif msg.video:
        await context.bot.send_video(
            CHANNEL_ID,
            msg.video.file_id,
            caption=f"Dari {sender}:\n{msg.caption or ''}"
        )
    elif msg.document:
        await context.bot.send_document(
            CHANNEL_ID,
            msg.document.file_id,
            caption=f"Dari {sender}:\n{msg.caption or ''}"
        )

    logger.info(f"Pesan #profit diteruskan dari {sender}")

# =================== GREETINGS ===================
async def send_greeting(app, time_of_day):
    """time_of_day: 'pagi' | 'siang' | 'malam' """
    wib = pytz.timezone("Asia/Jakarta")
    now = datetime.datetime.now(wib)
    day_name = now.strftime("%A")
    day_map = {
        "Monday": "Senin",
        "Tuesday": "Selasa",
        "Wednesday": "Rabu",
        "Thursday": "Kamis",
        "Friday": "Jumat",
        "Saturday": "Sabtu",
        "Sunday": "Minggu",
    }
    hari = day_map.get(day_name, day_name)

    text = ""

    # =================== Senin - Jumat (XAUUSD mode) ===================
    if hari in ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]:
        if time_of_day == "pagi":
            text = f"Selamat pagi Traders dan selamat hari {hari}, mari kita berburu Dollar di XAUUSD ✨"
        elif time_of_day == "siang":
            text = "Selamat siang traders, jangan lupa makan siang terlebih dahulu agar ada tenaga untuk menganalisa chart XAUUSD 💪"
        elif time_of_day == "malam":
            if hari == "Jumat":
                text = ("Selamat malam trader, sudah waktunya istirahat. "
                        "Malam ini hari terakhir kita untuk menambang emas, kita akan lanjutkan Senin pagi lagi. "
                        "Tetapi jika ada yang hobi menambang BITCOIN boleh bangun besok pagi ya hehe 🚀")
            else:
                text = "Selamat malam trader, sudah waktunya istirahat. Jangan terlalu berlebihan untuk trading, mari kita lanjutkan besok lagi 🌙"

    # =================== Sabtu - Minggu (Bitcoin mode) ===================
    else:
        if time_of_day == "pagi":
            text = f"Selamat pagi Traders, selamat hari {hari}, saatnya kita berburu Dollar di Bitcoin 🚀"
        elif time_of_day == "siang":
            text = "Selamat siang traders, jangan lupa makan siang. Kita lanjut analisa chart Bitcoin sore ini 💪"
        elif time_of_day == "malam":
            text = "Selamat malam trader, sudah waktunya istirahat. Jangan terlalu berlebihan untuk trading Bitcoin, lanjut besok lagi 🌙"

    # Kirim ke Grup & Channel
    if text:
        await app.bot.send_message(GROUP_ID, text)
        await app.bot.send_message(CHANNEL_ID, text)
        logger.info(f"Pesan greeting '{time_of_day}' dikirim ({hari})")

    # Tambahan promo khusus malam → hanya ke channel
    if time_of_day == "malam":
        promo = (
            "Untuk Bergabung Ke GRUP SIGNAL AI & GRUP NEWS AI , DAN IKUTAN PROFIT SEPERTI TEMAN TEMAN YANG LAIN.\n"
            "KALIAN BISA CHAT ADMIN TELEGRAM YA  GRATISS ✅"
        )
        await app.bot.send_message(CHANNEL_ID, promo)
        logger.info("Promo malam dikirim ke channel")

# =================== MAIN ===================
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Handler untuk forward pesan dari grup private
    app.add_handler(MessageHandler(filters.Chat(GROUP_ID), forward_testi))

    # Scheduler greetings (WIB)
    scheduler = AsyncIOScheduler(timezone="Asia/Jakarta")
    scheduler.add_job(send_greeting, "cron", hour=7, minute=0, args=[app, "pagi"])   # 07:00 WIB
    scheduler.add_job(send_greeting, "cron", hour=12, minute=0, args=[app, "siang"]) # 12:00 WIB
    scheduler.add_job(send_greeting, "cron", hour=21, minute=0, args=[app, "malam"]) # 21:00 WIB
    scheduler.start()
    logger.info("Scheduler started")

    # Jalankan bot polling
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

# =================== RUN SCRIPT ===================
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(main())
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
