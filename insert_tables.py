import psycopg2
from dbmanage import connectdb

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
import logging

# Все для выбора вывода, ввода, удаления и изменения
WORKERS, CARS, SHOPS, ORDERS, CHOICE = range(5)

logger = logging.getLogger(__name__)

async def insert_workers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    conn = connectdb()
    text = update.message.text
    try:
        fio, skips, position, experience, pay = text.split(", ")
        logger.info("Got from user: %s, %s, %s, %s, %s", fio, position, experience, skips, pay)
    except Exception as error:
        logger.info(error)
        await update.message.reply_text("Неправильный ввод! попробуйте снова")
        return WORKERS
    with conn.cursor() as cur:
        try:
            cur.execute("INSERT INTO workers VALUES (DEFAULT, %s, %s, %s, %s)", (fio, position, int(experience), int(skips)))
        except psycopg2.errors.ForeignKeyViolation as e:
            cur.execute("ROLLBACK", (position, int(experience), int(pay)))
            cur.execute("INSERT INTO positions VALUES (%s, %s, %s)", (position, int(experience), int(pay)))
            cur.execute("INSERT INTO workers VALUES (DEFAULT, %s, %s, %s, %s)", (fio, position, int(experience), int(skips)))
        conn.commit()
    conn.close()
    await update.message.reply_text("Готово!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
        
async def insert_cars(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    conn = connectdb()
    text = update.message.text
    try:
        vin, brand, name, year, colour, colourType, body, price = text.split(", ")
        logger.info("Got from user: %s, %s, %s, %s, %s", vin, brand, name, year, colour, colourType, body, price)
    except Exception as error:
        logger.info(error)
        await update.message.reply_text("Неправильный ввод! попробуйте снова")
        return WORKERS
    with conn.cursor() as cur:
        try:
            cur.execute("INSERT INTO cars VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (vin, brand, name, int(year), colour, colourType, body, int(price)))
        except psycopg2.errors.ForeignKeyViolation as e:
            print(e)
        conn.commit()
    conn.close()
    await update.message.reply_text("Готово!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
    
async def insert_shops(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    conn = connectdb()
    text = update.message.text
    try:
        name, address, city, rating = text.split(", ")
        logger.info("Got from user: %s, %s, %s, %s", name, address, city, rating)
    except Exception as error:
        logger.info(error)
        await update.message.reply_text("Неправильный ввод! попробуйте снова")
        return WORKERS
    with conn.cursor() as cur:
        try:
            cur.execute("INSERT INTO shops VALUES (DEFAULT, %s, %s, %s, %s)", (name, address, city, rating))
        except psycopg2.errors.ForeignKeyViolation as e:
            print(e)
        conn.commit()
    conn.close()
    await update.message.reply_text("Готово!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
