from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# === CẤU HÌNH BOT ===
BOT_TOKEN = "6905338053:AAFptL1O2KuOHg7jMOsUV10cOUCVHAgmiGU"
SHEET_API = "https://script.google.com/macros/s/AKfycbzT6nZo9BL04qE0MwyYIzNnhzQ6AnSXzTDl8-WzAA-a86rS1MycPubfh5pgGsu1IvDmLA/exec"  # link web app từ Google Apps Script

# === HÀM KHI GÕ /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Xin chào! Gửi mã cần tra cứu (ví dụ: NV001)")

# === HÀM TRA CỨU DỮ LIỆU ===
async def query_sheet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    res = requests.get(SHEET_API, params={'q': text})
    data = res.json()

    if "error" in data:
        reply = f"❌ {data['error']}"
    else:
        reply = (
            f"✅ *{data['MA_NV']} - {data['TEN_NV']}*\n"
            f"👤 Giới tính: {data['Giới tính']}\n"
            f"🎂 Ngày sinh: {data['Ngày sinh']}\n"
            f"🪪 BHXH: {data['BHXH']}"
        )
    await update.message.reply_text(reply, parse_mode="Markdown")

# === CHẠY BOT ===
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, query_sheet))

print("🤖 Bot đang chạy... Nhấn Ctrl+C để dừng.")
app.run_polling()
