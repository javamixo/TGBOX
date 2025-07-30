import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from categories import CHANNELS

# Load bot token from environment variable
TOKEN = os.environ.get("BOT_TOKEN")

# Logging config
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(category, callback_data=category)]
        for category in CHANNELS.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📺 Welcome to TV Box!\nChoose a category:", reply_markup=reply_markup)

# Callback query handler
async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data
    channels = CHANNELS.get(category, [])
    response = f"📡 *{category} Channels:*\n\n"
    for title, url in channels:
        response += f"🔗 [{title}]({url})\n"
    await query.edit_message_text(response, parse_mode="Markdown", disable_web_page_preview=True)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(category_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
