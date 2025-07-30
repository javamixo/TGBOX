# main.py

import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from categories import CHANNELS

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("BOT_TOKEN")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(name, callback_data=name)] for name in CHANNELS.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🎬 Welcome to your personal TV Box!\nChoose a category:",
        reply_markup=reply_markup
    )

# Handle category selection
async def handle_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data
    channels = CHANNELS.get(category, [])

    if not channels:
        await query.edit_message_text("No channels available in this category yet.")
        return

    response = f"📺 *{category} Channels:*\n\n"
    for name, url in channels:
        response += f"🔗 [{name}]({url})\n"

    await query.edit_message_text(
        text=response,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_category))
    print("Bot is running... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == '__main__':
    main()
