import psycopg2
from dbmanage import connectdb

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
import logging

# Все для выбора вывода, ввода, удаления и изменения
BUYERS, WORKERS, JOBS, CARS, SHOPS, DEALERS, ORDERS, CHOICE, TYPING_UPDATE = range(9)

logger = logging.getLogger(__name__)

async def insert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Покупатели", "Сотрудники", "Должности", "Автомобили", "Автосалоны", "Поставщики", "Заказы"]]
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
        case "Покупатели":
            await update.message.reply_text("Введите: ФИО, Телефон")
            return BUYERS
        case "Сотрудники":
            await update.message.reply_text("Введите: ФИО, Пропуски, Должность, Опыт")
            return WORKERS
        case "Автомобили":
            await update.message.reply_text("Введите: VIN, Марка, Название, Год, Цвет, Покраска, Кузов, Цена")
            return CARS
        case "Автосалоны":
            await update.message.reply_text("Введите: Название, Улица, Город, Рейтинг")
            return SHOPS
        case "Заказы":
            await update.message.reply_text("Введите: ИД магазина, ИД сотрудника, VIN, ИД покупателя, ИД поставщика, Адрес доставки, Итоговая цена")
            return ORDERS
        case "Должности":
            await update.message.reply_text("Введите: Должность, Опыт, Зарплата")
            return JOBS
        case "Поставщики":
            await update.message.reply_text("Введите: Название, Страна, Регион, Город, Адрес")
            return DEALERS
    logger.info("Printing to %s: %s", update.message.from_user.first_name, result)
    await update.message.reply_text(result, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def insert_buyers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    try:
        fio, phone, = text.split(", ")
        logger.info("Got from user: %s, %s, ", fio, phone)
    except ValueError as e:
        logger.info(e)
        await update.message.reply_text("Ошибка ввода данных! Попробуйте снова")
        return BUYERS
    conn = connectdb()
    with conn.cursor() as cur:
        cur.execute("INSERT INTO buyers VALUES (DEFAULT, %s, %s)", (fio, phone))
        conn.commit()
    conn.close()
    await update.message.reply_text("Готово!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def insert_workers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    try:
        fio, skips, position, experience = text.split(", ")
        logger.info("Got from user: %s, %s, %s, %s", fio, position, experience, skips)
        experience, skips = int(experience), int(skips)
    except ValueError as e:
        logger.info(e)
        await update.message.reply_text("Ошибка ввода данных! Попробуйте снова")
        return WORKERS
    conn = connectdb()
    with conn.cursor() as cur:
        try:
            cur.execute("INSERT INTO workers VALUES (DEFAULT, %s, %s, %s, %s)", (fio, position, experience, skips))
        except psycopg2.errors.ForeignKeyViolation as e:
            await update.message.reply_text("Неизвестная должность! Таблица не изменена.")
        conn.commit()
    conn.close()
    await update.message.reply_text("Готово!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def insert_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    try:
        position, experience, pay = text.split(", ")
        logger.info("Got from user: %s, %s, %s", position, experience, pay)
        experience, paY = int(experience), int(pay)
    except ValueError as e:
        logger.info(e)
        await update.message.reply_text("Ошибка ввода данных! Попробуйте снова")
        return JOBS
    conn = connectdb()
    with conn.cursor() as cur:
        try:
            cur.execute("INSERT INTO positions VALUES (%s, %s, %s)", (position, experience, pay))
        except psycopg2.errors.UniqueViolation as e:
            await update.message.reply_text("Такая должность уже известна! Таблица не изменена.")
        conn.commit()
    conn.close()
    await update.message.reply_text("Готово!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
        
async def insert_cars(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    try:
        vin, brand, name, year, colour, colourType, body, price = text.split(", ")
        logger.info("Got from user: %s", (vin, brand, name, year, colour, colourType, body, price))
        vin, year, price = int(vin), int(year), int(price)
    except ValueError as e:
        logger.info(e)
        await update.message.reply_text("Ошибка ввода данных! Попробуйте снова")
        return CARS
    conn = connectdb()
    with conn.cursor() as cur:
        try:
            cur.execute("INSERT INTO cars VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (vin, brand, name, year, colour, colourType, body, price))
        except psycopg2.errors.UniqueViolation as e:
            await update.message.reply_text("Машина с таким VIN кодом уже известна! Таблица не изменена.")
        conn.commit()
    conn.close()
    await update.message.reply_text("Готово!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
    
async def insert_shops(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    try:
        name, address, city, rating = text.split(", ")
        logger.info("Got from user: %s, %s, %s, %s", name, address, city, rating)
        rating = int(rating)
    except ValueError as e:
        logger.info(e)
        await update.message.reply_text("Ошибка ввода данных! Попробуйте снова")
        return SHOPS
    conn = connectdb()
    with conn.cursor() as cur:
        cur.execute("INSERT INTO shops VALUES (DEFAULT, %s, %s, %s, %s)", (name, address, city, rating))
        conn.commit()
    conn.close()
    await update.message.reply_text("Готово!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def insert_dealers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    try:
        name, country, region, city, address = text.split(", ")
        logger.info("Got from user: %s, %s, %s, %s, %s", name, country, region, city, address)
    except ValueError as e:
        logger.info(e)
        await update.message.reply_text("Ошибка ввода данных! Попробуйте снова")
        return DEALERS
    conn = connectdb()
    with conn.cursor() as cur:
        cur.execute("INSERT INTO dealers VALUES (DEFAULT, %s, %s, %s, %s, %s)", (name, country, region, city, address))
        conn.commit()
    conn.close()
    await update.message.reply_text("Готово!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def insert_orders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    try:
        shopId, workerId, vin, buyerId, dealerId, deliveryAddr, totalPrice = text.split(", ")
        logger.info("Got from user: %s", shopId, workerId, vin, buyerId, deliveryAddr, dealerId, totalPrice)
        shopId, workerId, vin, buyerId, dealerId, totalPrice = int(shopId), int(workerId), int(vin), int(buyerId), int(dealerId), int(totalPrice)
    except ValueError as e:
        logger.info(e)
        await update.message.reply_text("Ошибка ввода данных! Попробуйте снова")
        return ORDERS
    conn = connectdb()
    with conn.cursor() as cur:
        try:
            cur.execute("INSERT INTO total_prices VALUES (%s, %s, %s, %s, %s, %s)", (shopId, vin, buyerId, deliveryAddr, dealerId, totalPrice))
            cur.execute("INSERT INTO keys_table VALUES (%s, %s, %s, %s, %s, %s)", (shopId, workerId, vin, buyerId, deliveryAddr, dealerId))
        except psycopg2.errors.ForeignKeyViolation as e:
            await update.message.reply_text("Неизвестный автосалон/сотрудник/авто/покупатель/поставщик. Таблица не изменена.")
        except psycopg2.errors.UniqueViolation as e:
            await update.message.reply_text("Такой заказ уже известен! Таблица не изменена.")
        conn.commit()
    conn.close()
    await update.message.reply_text("Готово!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END