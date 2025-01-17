import os
from dotenv import load_dotenv

import psycopg2

from show_tables import show_workers, show_cars, show_shops, show_orders
#from insert_tables import insert_workers, insert_cars, insert_shops, insert_orders

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

WORKERS, BUYERS, DEALERS, CARS, SHOPS, ORDERS, CHOICE, TYPING_REPLY = range(8)

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
    await update.message.reply_text("/start, /view, /insert")

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
    
async def select_view(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Отмена.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def insert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    #reply_keyboard = [["Сотрудники", "Автомобили", "Автосалоны", "Заказы"]]
    reply_keyboard = [["Сотрудники"]]
    await update.message.reply_text(
        "В какую таблицу вставить данные?\n"
        "/cancel для отмены",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Выбор"
        ),
    )
    return CHOICE
    
async def select_insert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    logger.info("Got text: %s", text)
    if "table" not in context.user_data:
        context.user_data["table"] = text
        logger.info("That's a table's name.")
    else:
        info = context.user_data["info"]
        context.user_data[info] = text
        logger.info("Table known, writing info.")
    match context.user_data["table"]:
        case "Сотрудники":
            return WORKERS
        case "Автомобили":
            return CARS
        case "Автосалоны":
            return SHOPS
        case "Заказы":
            return ORDERS
    return ConversationHandler.END

async def insert_workers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    for i in ["ФИО", "должность", "опыт", "пропуски"]:
        if i not in context.user_data:
            context.user_data["info"] = i
            await update.message.reply_text("Введите")
            await update.message.reply_text(i)
            return WORKERS
    fio = context.user_data["ФИО"]
    position = context.user_data["должность"]
    experience = context.user_data["опыт"]
    skips = context.user_data["пропуски"]
    with conn.cursor() as cur:
        try:
            cur.execute("INSERT INTO workers VALUES (DEFAULT, %s, %s, %s, %s)", (fio, position, experience, skips))
        except psycopg2.errors.ForeignKeyViolation as e:
            if "зарплату" not in context.user_data:
                context.user_data["info"] = "зарплату"
                await update.message.reply_text("Введите")
                await update.message.reply_text(i)
                return WORKERS
            pay = context.user_data["зарплату"]
            cur.execute("INSERT INTO positions VALUES (DEFAULT, %s, %s, %s, %s)", (position, experience, pay))
            cur.execute("INSERT INTO workers VALUES (DEFAULT, %s, %s, %s, %s)", (fio, position, experience, skips))
            del context.user_data["зарплату"]
        conn.commit()
    del context.user_data["ФИО"]
    del context.user_data["должность"]
    del context.user_data["опыт"]
    del context.user_data["пропуски"]
    del context.user_data["table"]
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
    
    insert_handler = ConversationHandler(
        entry_points=[CommandHandler("insert", insert)],
        states={
            CHOICE: [MessageHandler(filters.Regex("^(Сотрудники|Автомобили|Автосалоны|Заказы)$"), select_insert)],
            WORKERS: [MessageHandler(filters.TEXT, insert_workers)],
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
