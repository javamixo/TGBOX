import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from categories import CHANNELS

# Load token from environment variable
TOKEN = os.environ.get("BOT_TOKEN")

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(name, callback_data=name)] for name in CHANNELS.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎬 Welcome to your TV Box!\nChoose a category:", reply_markup=reply_markup)

# Handle category button click
async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data
    channels = CHANNELS.get(category, [])
    response = f"📺 *{category} Channels:*\n\n"
    for title, url in channels:
        response += f"🔗 [{title}]({url})\n"
    await query.edit_message_text(text=response, parse_mode="Markdown", disable_web_page_preview=True)

# Main entry point
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(category_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
