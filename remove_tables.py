import psycopg2

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode
import logging

from tabulate import tabulate

from show_tables import show_orders
from dbmanage import connectdb

# Все для выбора вывода, ввода, удаления и изменения
BUYERS, WORKERS, JOBS, CARS, SHOPS, DEALERS, ORDERS, CHOICE = range(8)

logger = logging.getLogger(__name__)

from show_tables import show_workers, show_cars, show_shops, show_orders, show_jobs, show_dealers, show_buyers

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Покупатели", "Сотрудники", "Должности", "Автомобили", "Автосалоны", "Поставщики", "Заказы"]]
    await update.message.reply_text(
        "Из какой таблицу вы хотите удалить данные?\n"
        "/cancel для отмены",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Выбор"
        ),
    )
    return CHOICE

async def selected_remove(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Selected insert: %s", update.message.text)
    result="Ошибка"
    headers=["Ошибка"]
    text = update.message.text
    context.user_data["table"] = text
    match text:
        case "Покупатели":
            result = show_buyers()
            headers = ["ИД", "ФИО", "Телефон"]
        case "Сотрудники":
            result = show_workers()
            headers = ["ИД", "ФИО", "Пропуски", "Должность", "Опыт", "Зарплата"]
        case "Должности":
            result = show_jobs()
            headers = ["Должность", "Опыт", "Зарплата"]
        case "Автомобили":
            result = show_cars()
            headers = ["VIN", "Марка", "Название", "Год", "Цвет", "Покраска", "Кузов", "Цена"]
        case "Автосалоны":
            result = show_shops()
            headers = ["ИД", "Название", "Улица", "Город", "Рейтинг"]
        case "Поставщики":
            result = show_dealers()
            headers = ["ИД", "Название", "Страна", "Регион", "Город", "Адрес"]
        case "Заказы":
            result = show_orders()
            headers = ["Магазин", "Адрес", "Сотрудник", "Марка", "Авто", "Покупатель", "Итоговая цена"]
    result = tabulate(result, headers=headers)
    await update.message.reply_text(f'<pre>{result}</pre>', parse_mode=ParseMode.HTML)
    match text:
        case "Покупатели":
            await update.message.reply_text("Введите ИД покупателя: ")
            return BUYERS
        case "Сотрудники":
            await update.message.reply_text("Введите ИД сотрудника: ")
            return WORKERS
        case "Должности":
            await update.message.reply_text("Введите ИД должности: ")
            return JOBS
        case "Автомобили":
            await update.message.reply_text("Введите VIN: ")
            return CARS
        case "Автосалоны":
            await update.message.reply_text("Введите ИД автосалона: ")
            return SHOPS
        case "Поставщики":
            await update.message.reply_text("Введите название поставщика: ")
            return DEALERS
        case "Заказы":
            await update.message.reply_text("Введите что-нибудь: ")
            return ORDERS
    return ConversationHandler.END

async def remove_buyers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("PLACEHOLDER")
    return ConversationHandler.END

async def remove_workers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        inputId = int(update.message.text)
        logger.info("Got from user: %s ", inputId)
    except Exception as error:
        logger.info(error)
        await update.message.reply_text("Неправильный ввод! попробуйте снова")
        return WORKERS
    conn = connectdb()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM workers WHERE workerId = (%s)", (inputId,))
        conn.commit()
    conn.close()
    await update.message.reply_text("Готово!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def remove_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("PLACEHOLDER")
    return ConversationHandler.END

async def remove_cars(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("PLACEHOLDER")
    return ConversationHandler.END

async def remove_shops(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("PLACEHOLDER")
    return ConversationHandler.END

async def remove_dealers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("PLACEHOLDER")
    return ConversationHandler.END

async def remove_orders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("PLACEHOLDER")
    return ConversationHandler.END