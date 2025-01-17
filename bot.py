import os
from dotenv import load_dotenv

import psycopg2

from show_tables import show_workers, show_cars, show_shops, show_orders

import logging
from telegram import ForceReply, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

WORKERS, BUYERS, DEALERS, CARS, SHOPS, ORDERS, CHOICE = range(7)

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("/start, /view, /insert")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

async def view(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Сотрудники", "Автомобили", "Автосалоны", "Заказы"]]
    await update.message.reply_text(
        "Что вы хотите просмотреть?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Выбор"
        ),
    )
    return CHOICE
    
async def select_view(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Selected view: %s", update.message.text)
    result = "Ошибка"
    match update.message.text:
        case "Сотрудники":
            result = show_workers()
        case "Автомобили":
            result = show_cars()
        case "Автосалоны":
            result = show_shops()
        case "Заказы":
            result = show_orders()
    #result = [(x.encode('utf-8') for x in tup) for tup in result]
    logger.info("Printing to %s: %s", update.message.from_user, result)
    await update.message.reply_text(result)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Отмена.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv("API_KEY")).build()
    
    view_handler = ConversationHandler(
        entry_points=[CommandHandler("view", view)],
        states={
            CHOICE: [MessageHandler(filters.Regex("^(Сотрудники|Автомобили|Автосалоны|Заказы)$"), select_view)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    # Conversation handlers
    application.add_handler(view_handler)
    
    # Help command
    application.add_handler(CommandHandler("help", help_command))
    
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":
    main()
