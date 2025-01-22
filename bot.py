import os
from dotenv import load_dotenv

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

from dbmanage import connectdb

from show_tables import view, selected_view, show_workers, show_cars, show_shops, show_orders, show_jobs, show_dealers, show_buyers
from insert_tables import insert, selected_insert, insert_workers, insert_cars, insert_shops, insert_orders, insert_jobs, insert_dealers, insert_buyers
from remove_tables import remove, selected_remove, remove_workers, remove_cars, remove_shops, remove_orders, remove_jobs, remove_dealers, remove_buyers
from update_tables import update, selected_update, update_workers, typing_update, update_cars, update_shops, update_orders, update_jobs, update_dealers, update_buyers

load_dotenv() #Загрузить приватную инфу

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Все для выбора вывода, ввода, удаления и изменения
BUYERS, WORKERS, JOBS, CARS, SHOPS, DEALERS, ORDERS, CHOICE, TYPING_UPDATE = range(9)

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!"
        "\n/start, /view, /insert, /remove, /update",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "/start - команда первого запуска\n"
        "/view - обзор некоторых баз данных\n"
        "/insert - вставить информацию\n"
        "/remove - удалить информацию\n"
        "/update - обновить информацию\n"
        )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

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
            CHOICE: [MessageHandler(filters.Regex("^(Покупатели|Сотрудники|Должности|Автомобили|Автосалоны|Поставщики|Заказы)$"), selected_view)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    insert_handler = ConversationHandler(
        entry_points=[CommandHandler("insert", insert)],
        states={
            CHOICE: [MessageHandler(filters.Regex("^(Покупатели|Сотрудники|Должности|Автомобили|Автосалоны|Поставщики|Заказы)$"), selected_insert)],
            BUYERS: [MessageHandler(filters.TEXT & (~ filters.COMMAND), insert_buyers)],
            WORKERS: [MessageHandler(filters.TEXT & (~ filters.COMMAND), insert_workers)],
            JOBS: [MessageHandler(filters.TEXT & (~ filters.COMMAND), insert_jobs)],
            CARS: [MessageHandler(filters.TEXT & (~ filters.COMMAND), insert_cars)],
            SHOPS: [MessageHandler(filters.TEXT & (~ filters.COMMAND), insert_shops)],
            DEALERS: [MessageHandler(filters.TEXT & (~ filters.COMMAND), insert_dealers)],
            ORDERS: [MessageHandler(filters.TEXT & (~ filters.COMMAND), insert_orders)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    remove_handler = ConversationHandler(
        entry_points=[CommandHandler("remove", remove)],
        states={
            CHOICE: [MessageHandler(filters.Regex("^(Покупатели|Сотрудники|Должности|Автомобили|Автосалоны|Поставщики|Заказы)$"), selected_remove)],
            BUYERS: [MessageHandler(filters.TEXT & (~ filters.COMMAND), remove_buyers)],
            WORKERS: [MessageHandler(filters.TEXT & (~ filters.COMMAND), remove_workers)],
            JOBS: [MessageHandler(filters.TEXT & (~ filters.COMMAND), remove_jobs)],
            CARS: [MessageHandler(filters.TEXT & (~ filters.COMMAND), remove_cars)],
            SHOPS: [MessageHandler(filters.TEXT & (~ filters.COMMAND), remove_shops)],
            ORDERS: [MessageHandler(filters.TEXT & (~ filters.COMMAND), remove_orders)],
            DEALERS: [MessageHandler(filters.TEXT & (~ filters.COMMAND), remove_dealers)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    update_handler = ConversationHandler(
        entry_points=[CommandHandler("update", update)],
        states={
            CHOICE: [MessageHandler(filters.Regex("^(Покупатели|Сотрудники|Должности|Автомобили|Автосалоны|Поставщики|Заказы)$"), selected_update)],
            TYPING_UPDATE: [MessageHandler(filters.TEXT & (~ filters.COMMAND), typing_update)],
            BUYERS: [MessageHandler(filters.TEXT & (~ filters.COMMAND), update_buyers)],
            WORKERS: [MessageHandler(filters.TEXT & (~ filters.COMMAND), update_workers)],
            JOBS: [MessageHandler(filters.TEXT & (~ filters.COMMAND), update_jobs)],
            CARS: [MessageHandler(filters.TEXT & (~ filters.COMMAND), update_cars)],
            SHOPS: [MessageHandler(filters.TEXT & (~ filters.COMMAND), update_shops)],
            ORDERS: [MessageHandler(filters.TEXT & (~ filters.COMMAND), update_orders)],
            DEALERS: [MessageHandler(filters.TEXT & (~ filters.COMMAND), update_dealers)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    # Conversation handlers
    application.add_handler(view_handler)
    application.add_handler(insert_handler)
    application.add_handler(remove_handler)
    application.add_handler(update_handler)
    
    # Start command
    application.add_handler(CommandHandler("start", start))
    
    # Help command
    application.add_handler(CommandHandler("help", help_command))
    
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":
    main()
