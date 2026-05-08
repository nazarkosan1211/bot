# =======================
# bot.py Railway + Web App Button
# =======================

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

# =======================
# CONFIG
# =======================
API_URL = "https://server-production-30a5.up.railway.app"
WEB_APP_URL = "https://inspiring-puppy-392097.netlify.app/"

BOT_TOKEN = "8707863883:AAGePtyGNttlo3EfLT1GXGKlBqFY9TBQ5G0"

# =======================
# HELPER
# =======================
def post_to_server(endpoint, payload):
    try:
        res = requests.post(f"{API_URL}/{endpoint}", json=payload, timeout=15)
        return res.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

def make_webapp_button(user_id):
    web_url = f"{WEB_APP_URL}?ref={user_id}"

    keyboard = [
        [
            InlineKeyboardButton(
                text="🚀 Open EarnFlow",
                web_app=WebAppInfo(url=web_url)
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)

# =======================
# COMMAND /start
# =======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)

    ref = None
    if context.args:
        start_param = context.args[0]
        if start_param.startswith("ref_"):
            ref = start_param.replace("ref_", "")

    payload = {
        "user_id": user_id,
        "ref": ref
    }

    res = post_to_server("start_user", payload)

    username = user.username if user.username else "User"

    if res.get("status") in ["success", "ok"]:
        text = (
            f"Hello @{username}! 👋\n\n"
            f"✅ Kamu sudah terdaftar di EarnFlow.\n"
            f"🆔 User ID: {user_id}\n\n"
            f"Klik tombol di bawah untuk buka aplikasi."
        )
    else:
        text = (
            f"⚠️ Server merespon error:\n"
            f"{res.get('message', res)}\n\n"
            f"Tapi kamu tetap bisa coba buka aplikasi."
        )

    await update.message.reply_text(
        text,
        reply_markup=make_webapp_button(user_id)
    )

# =======================
# COMMAND /task TEST
# =======================
async def task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    payload = {
        "user_id": user_id,
        "amount": 1
    }

    res = post_to_server("add_coin", payload)

    if res.get("status") == "success":
        await update.message.reply_text(
            f"✅ Task berhasil!\n\n"
            f"Coins: {res.get('coins')}\n"
            f"Tasks Done: {res.get('tasks_done')}\n"
            f"Remaining Tasks: {res.get('remaining_tasks')}"
        )
    elif res.get("status") == "blocked":
        reason = res.get("reason")

        if reason == "cooldown":
            await update.message.reply_text(
                f"⏳ Tunggu {res.get('wait')} detik dulu sebelum task lagi."
            )
        else:
            await update.message.reply_text(
                "🚫 Limit daily task tercapai. Tunggu besok."
            )
    else:
        await update.message.reply_text(
            f"❌ Error:\n{res.get('message', res)}"
        )

# =======================
# MAIN
# =======================
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("task", task))

    print("Bot running with Web App button...")
    app.run_polling()
