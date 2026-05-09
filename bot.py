# =========================================
# EarnFlow Telegram Bot (Global Version)
# =========================================

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

import requests

# =========================================
# CONFIG
# =========================================

BOT_TOKEN = "8707863883:AAGePtyGNttlo3EfLT1GXGKlBqFY9TBQ5G0"

API_URL = "https://server-production-30a5.up.railway.app"

WEB_APP_URL = "https://moonlit-pie-98038d.netlify.app/"

# =========================================
# SERVER REQUEST
# =========================================

def post_to_server(endpoint, payload):

    try:

        response = requests.post(
            f"{API_URL}/{endpoint}",
            json=payload,
            timeout=15
        )

        return response.json()

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }

# =========================================
# WEB APP BUTTON
# =========================================

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

# =========================================
# /START
# =========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    user_id = str(user.id)

    username = user.username if user.username else "User"

    ref = None

    # Referral Detect
    if context.args:

        start_param = context.args[0]

        if start_param.startswith("ref_"):

            ref = start_param.replace("ref_", "")

    # Register User
    payload = {
        "user_id": user_id,
        "ref": ref
    }

    result = post_to_server("start_user", payload)

    # Message
    if result.get("status") in ["success", "ok"]:

        text = (
            f"👋 Welcome @{username}!\n\n"

            f"🔥 Welcome to EarnFlow.\n"
            f"Complete tasks, earn points, and climb the leaderboard.\n\n"

            f"💎 Earn daily rewards\n"
            f"👥 Invite friends for bonus points\n"
            f"🏆 Compete with global users\n"
            f"🚀 More features coming soon\n\n"

            f"Tap the button below to open the app."
        )

    else:

        text = (
            f"⚠️ Server response error.\n\n"
            f"You can still try opening the app below."
        )

    await update.message.reply_text(
        text,
        reply_markup=make_webapp_button(user_id)
    )

# =========================================
# MAIN
# =========================================

if __name__ == "__main__":

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Only /start command
    app.add_handler(CommandHandler("start", start))

    print("EarnFlow bot is running...")

    app.run_polling()
