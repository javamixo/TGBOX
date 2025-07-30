import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from categories import CHANNELS

TOKEN = os.environ.get("BOT_TOKEN")  # Use env variable on Render

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(name, callback_data=name)] for name in CHANNELS.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎬 Welcome to your TV Box!\nChoose a category:", reply_markup=reply_markup)

# Category selection handler
async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data
    channels = CHANNELS.get(category, [])
    response = f"📺 *{category} Channels:*\n\n"
    for title, url in channels:
        response += f"🔗 [{title}]({url})\n"
    await query.edit_message_text(text=response, parse_mode="Markdown", disable_web_page_preview=True)

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(category_handler))
    application.run_polling()

if __name__ == '__main__':
    main()
