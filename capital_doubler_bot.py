
import logging
import requests
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "7817543208:AAEzFO6GaWx_5OXOLfEpXAOHOCCVaSqtlbk"
CHANNEL_USERNAME = "@globalinvestmentt"
RECEIVER_WALLET = "TJEUJySFwBqZzDteWEe31DphZfMHTGfAqy"
NOWPAYMENTS_API_KEY = "N06TDAK-ZNYMMJF-GB3G90T-X1ZWESW"
NOWPAYMENTS_IPN_KEY = "uRf+Empf431uErq75yHaqjMV7NdMDgI5"

app = Flask(__name__)

users_db = {}
referrals = {}

def create_invoice(user_id):
    url = "https://api.nowpayments.io/v1/invoice"
    headers = {
        "x-api-key": NOWPAYMENTS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "price_amount": 20,
        "price_currency": "usd",
        "pay_currency": "usdttrc20",
        "ipn_callback_url": "https://yourdomain.com/ipn",
        "order_id": str(user_id),
        "order_description": "Capital Doubler Access"
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = "👋 Welcome to Capital Doubler Bot!\n\nJoin our channel to continue:\n" + CHANNEL_USERNAME
    if context.args:
        ref_id = context.args[0]
        if ref_id != str(user_id):
            referrals[user_id] = int(ref_id)
    users_db.setdefault(user_id, {"verified": False, "paid": False, "refs": []})
    await context.bot.send_message(chat_id=user_id, text=text)

async def check_joined(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
    if chat_member.status in ["member", "administrator", "creator"]:
        invoice = create_invoice(user_id)
        await context.bot.send_message(chat_id=user_id, text=f"💰 Pay 20 USDT to this invoice:\n{invoice['invoice_url']}")
    else:
        await context.bot.send_message(chat_id=user_id, text="❌ You must join the channel to proceed.")

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data = users_db.get(user_id, {})
    if user_data.get("verified", False) and len(user_data.get("refs", [])) >= 3:
        await context.bot.send_message(chat_id=user_id, text="✅ You can now withdraw your earnings. Please contact admin.")
    else:
        await context.bot.send_message(chat_id=user_id, text="❌ You need at least 3 verified referrals to withdraw.")

@app.route("/ipn", methods=["POST"])
def ipn():
    data = request.json
    if data.get("ipn_type") == "invoice" and data.get("payment_status") == "confirmed":
        user_id = int(data["order_id"])
        if user_id in users_db:
            users_db[user_id]["verified"] = True
            users_db[user_id]["paid"] = True
            ref_id = referrals.get(user_id)
            if ref_id and ref_id in users_db:
                users_db[ref_id]["refs"].append(user_id)
    return "OK"

def run_bot():
    logging.basicConfig(level=logging.INFO)
    app_tg = ApplicationBuilder().token(BOT_TOKEN).build()
    app_tg.add_handler(CommandHandler("start", start))
    app_tg.add_handler(CommandHandler("joined", check_joined))
    app_tg.add_handler(CommandHandler("withdraw", withdraw))
    app_tg.run_polling()

if __name__ == "__main__":
    import threading
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=5000)
