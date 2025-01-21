import psycopg2

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode
import logging

from tabulate import tabulate

from dbmanage import connectdb

# Все для выбора вывода, ввода, удаления и изменения
BUYERS, WORKERS, JOBS, CARS, SHOPS, DEALERS, ORDERS, CHOICE, TYPING_UPDATE = range(9)

logger = logging.getLogger(__name__)

async def view(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Покупатели", "Сотрудники", "Должности", "Автомобили", "Автосалоны", "Поставщики", "Заказы"]]
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
    result="Ошибка"
    headers=["Ошибка"]
    match update.message.text:
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
    logger.info("Printing to %s: %s", update.message.from_user.first_name, result)
    result = tabulate(result, headers=headers)
    await update.message.reply_text(f'<pre>{result}</pre>', parse_mode=ParseMode.HTML)
    return ConversationHandler.END

def show_buyers():
    conn = connectdb()
    with conn.cursor() as cur:
        cur.execute('''SELECT *
        FROM buyers 
        ORDER BY buyerId;''')
        result = cur.fetchall()
    conn.close()
    return result

def show_workers():
    conn = connectdb()
    with conn.cursor() as cur:
        cur.execute('''SELECT workers.workerId, workers.FIO, workers.skips, workers.position, workers.experience, positions.pay
        FROM workers
        INNER JOIN positions
        ON workers.position = positions.position AND workers.experience = positions.experience
        ORDER BY workers.workerId;''')
        result = cur.fetchall()
    conn.close()
    return result

def show_jobs():
    conn = connectdb()
    with conn.cursor() as cur:
        cur.execute('''SELECT *
        FROM positions
        ORDER BY position;''')
        result = cur.fetchall()
    conn.close()
    return result
        
def show_cars():
    conn = connectdb()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM cars ORDER BY cars.vin;")
        result = cur.fetchall()
    conn.close()
    return result
        
def show_shops():
    conn = connectdb()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM shops ORDER BY shops.shopId;")
        result = cur.fetchall()
    conn.close()
    return result

def show_dealers():
    conn = connectdb()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM dealers ORDER BY dealerId;")
        result = cur.fetchall()
    conn.close()
    return result
        
def show_orders():
    conn = connectdb()
    with conn.cursor() as cur:
        cur.execute('''SELECT s.name, s.address, w.FIO, c.brand, c.name, b.FIO, tp.totalPrice
        FROM keys_table AS kt
        CROSS JOIN total_prices AS tp
        INNER JOIN shops s ON kt.shopId = s.shopId AND tp.shopId = kt.shopId
        INNER JOIN workers w ON kt.workerId = w.workerId
        INNER JOIN cars c ON kt.vin = c.vin AND tp.vin = c.vin
        INNER JOIN buyers b ON kt.buyerId = b.buyerId AND tp.buyerId = b.buyerId
        INNER JOIN dealers d ON kt.dealerId = d.dealerId AND tp.dealerId = d.dealerId
        ;''')
        result = cur.fetchall()
    conn.close()
    return result