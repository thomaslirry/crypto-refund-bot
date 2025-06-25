from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "7128536142:AAE63mN10B2PAyLmhPnohPZzDY62XGXfX-E"

# Keyboard options
main_menu = [["Check Eligibility", "FAQ"], ["Talk to Support"]]

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    reply_markup = ReplyKeyboardMarkup(main_menu, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        f"Hello {user}, welcome to the General Refund Support Desk.\n\nChoose an option below to get started 👇",
        reply_markup=reply_markup
    )

# Check Eligibility handler
async def check_eligibility(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please enter the total amount you spent on digital assets over the past few years:")

# FAQ handler
async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "FAQs:\n\n1. What is this refund for?\n-> It's a refund process for qualified digital wallet users.\n\n"
        "2. Do I need to pay anything?\n-> You’ll only be asked to deposit a refundable % to verify the wallet.\n\n"
        "3. Is this legit?\n-> Yes. Verification is tied to the chain's records and compliance."
    )

# Talk to Support handler
async def talk_to_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("A support assistant will connect with you shortly. Please standby...")

# Main bot setup
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("Check Eligibility"), check_eligibility))
    app.add_handler(MessageHandler(filters.Regex("FAQ"), faq))
    app.add_handler(MessageHandler(filters.Regex("Talk to Support"), talk_to_support))

    app.run_polling()

if __name__ == "__main__":
    main()
