import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from keep_alive import keep_alive

# Load token securely from environment variable
TOKEN = os.environ["TOKEN"]

user_state = {}

# Main keyboard menu
main_menu = [["Check Eligibility", "FAQ"], ["Talk to Support"]]

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    reply_markup = ReplyKeyboardMarkup(
        main_menu, one_time_keyboard=True, resize_keyboard=True
    )
    await update.message.reply_text(
        f"Hello {user}, welcome to the General Refund Portal.\nPlease choose an option below 👇",
        reply_markup=reply_markup
    )

# Message handler logic
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user_id = update.effective_user.id

    if "eligibility" in text:
        await update.message.reply_text("Were you active in digital transactions between 2018 and 2023? (Yes/No)")
    elif text == "yes":
        await update.message.reply_text("Great! Please estimate how much you’ve spent in total (approximate value).")
        user_state[user_id] = "awaiting_amount"
    elif text == "no":
        await update.message.reply_text("No problem. If things change, feel free to check again.")
    elif user_state.get(user_id) == "awaiting_amount":
        user_state.pop(user_id)
        await update.message.reply_text(
            "Thank you. Based on your total, you may need to deposit a verification amount (about 20–30%) to initiate the refund process.\n\nWould you like to proceed?"
        )
    elif "faq" in text:
        await update.message.reply_text(
            "🔹 *FAQs*\n\n"
            "• Who is eligible?\n"
            "  Anyone who used digital assets from 2018–2023.\n\n"
            "• What do I need?\n"
            "  Only your original wallet or a verified transaction record.\n\n"
            "• Is there a fee?\n"
            "  There may be a verification deposit, fully refundable.\n\n"
            "Type 'Talk to Support' if you need help."
        )
    elif "support" in text:
        await update.message.reply_text("Our support team will connect with you shortly. Please standby.")
    else:
        await update.message.reply_text("Please select one of the menu options to proceed.")

# Run bot
if __name__ == "__main__":
    keep_alive()

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    app.run_polling()
