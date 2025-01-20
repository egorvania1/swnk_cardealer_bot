import psycopg2
from dbmanage import connectdb

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
import logging

# Все для выбора вывода, ввода, удаления и изменения
WORKERS, JOBS, CARS, SHOPS, DEALERS, ORDERS, BUYERS, CHOICE = range(8)

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
    result = "Ошибка"
    match update.message.text:
        case "Покупатели":
            result = show_buyers()
            await update.message.reply_text("ИД, ФИО, Телефон")
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
        case "Должности":
            result = show_jobs()
            await update.message.reply_text("Должность, Опыт, Зарплата")
        case "Поставщики":
            result = show_dealers()
            await update.message.reply_text("ИД, Название, Страна, Регион, Город, Адрес")
    logger.info("Printing to %s: %s", update.message.from_user.first_name, result)
    if type(result) == list:
        for x in result:
            await update.message.reply_text(x)
    else:
        await update.message.reply_text(result)
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