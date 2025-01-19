import os
from dotenv import load_dotenv

from show_tables import show_workers, show_cars, show_shops, show_orders
from insert_tables import insert_workers, insert_cars, insert_shops, insert_orders

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

load_dotenv() #Загрузить приватную инфу

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Все для выбора вывода, ввода, удаления и изменения
WORKERS, CARS, SHOPS, ORDERS, CHOICE = range(5)

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!"
        "\n/start, /view, /insert",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "/start - команда первого запуска\n"
        "/view - обзор некоторых баз данных\n"
        "/insert - вставить информацию о новых сотрудниках\n"
        )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

async def view(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Сотрудники", "Автомобили", "Автосалоны", "Заказы"]]
    await update.message.reply_text(
        "Что вы хотите просмотреть?\n"
        "/cancel для отмены",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Выбор"
        ),
    )
    return CHOICE
    
async def selected_view(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Selected view: %s", update.message.text)
    result = "Ошибка"
    match update.message.text:
        case "Сотрудники":
            result = show_workers()
            await update.message.reply_text("ИД, ФИО, Пропуски, Должность, Опыт, Зарплата")
        case "Автомобили":
            result = show_cars()
            await update.message.reply_text("VIN, Марка, Название, Год, Цвет, Покраска, Кузов, Цена")
        case "Автосалоны":
            result = show_shops()
            await update.message.reply_text("ИД, Название, Улица, Город, Рейтинг")
        case "Заказы":
            result = show_orders()
            await update.message.reply_text("Магазин, Сотрудник, Авто, Покупатель, Поставщик")
    logger.info("Printing to %s: %s", update.message.from_user.first_name, result)
    if type(result) == list:
        for x in result:
            await update.message.reply_text(x)
    else:
        await update.message.reply_text(result)
    return ConversationHandler.END

async def insert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Сотрудники", "Автомобили", "Автосалоны", "Заказы"]]
    await update.message.reply_text(
        "В какую таблицу вы хотите добавить данные?\n"
        "/cancel для отмены",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Выбор"
        ),
    )
    return CHOICE
    
async def selected_insert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Selected insert: %s", update.message.text)
    result = "Ошибка"
    match update.message.text:
        case "Сотрудники":
            result = show_workers()
            await update.message.reply_text("Введите: ФИО, Пропуски, Должность, Опыт, Зарплата")
            return WORKERS
        case "Автомобили":
            result = show_cars()
            await update.message.reply_text("Введите: VIN, Марка, Название, Год, Цвет, Покраска, Кузов, Цена")
            return CARS
        case "Автосалоны":
            result = show_shops()
            await update.message.reply_text("Введите: ИД, Название, Улица, Город, Рейтинг")
            return SHOPS
        case "Заказы":
            result = show_orders()
            await update.message.reply_text("Введите: ИД магазина, ИД сотрудника, VIN, ИД покупателя, ИД поставщика")
            return ORDERS
    logger.info("Printing to %s: %s", update.message.from_user.first_name, result)
    if type(result) == list:
        for x in result:
            await update.message.reply_text(x)
    else:
        await update.message.reply_text(result, reply_markup=ReplyKeyboardRemove())
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
            CHOICE: [MessageHandler(filters.Regex("^(Сотрудники|Автомобили|Автосалоны|Заказы)$"), selected_view)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    insert_handler = ConversationHandler(
        entry_points=[CommandHandler("insert", insert)],
        states={
            CHOICE: [MessageHandler(filters.Regex("^(Сотрудники|Автомобили|Автосалоны|Заказы)$"), selected_insert)],
            WORKERS: [MessageHandler(filters.TEXT, insert_workers)],
            CARS: [MessageHandler(filters.TEXT, insert_cars)],
            SHOPS: [MessageHandler(filters.TEXT, insert_shops)],
            ORDERS: [MessageHandler(filters.TEXT, insert_workers)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    # Conversation handlers
    application.add_handler(view_handler)
    application.add_handler(insert_handler)
    
    # Start command
    application.add_handler(CommandHandler("start", start))
    
    # Help command
    application.add_handler(CommandHandler("help", help_command))
    
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":
    main()
