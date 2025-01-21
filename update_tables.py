import psycopg2

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode
import logging

from tabulate import tabulate

from show_tables import show_orders
from dbmanage import connectdb

# Все для выбора вывода, ввода, удаления и изменения
BUYERS, WORKERS, JOBS, CARS, SHOPS, DEALERS, ORDERS, CHOICE, TYPING_UPDATE = range(9)

logger = logging.getLogger(__name__)

from show_tables import show_workers, show_cars, show_shops, show_orders, show_jobs, show_dealers, show_buyers

async def update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Покупатели", "Сотрудники", "Должности", "Автомобили", "Автосалоны", "Поставщики", "Заказы"]]
    await update.message.reply_text(
        "В какой таблице вы хотите обновить данные?\n"
        "/cancel для отмены",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Выбор"
        ),
    )
    return CHOICE

async def selected_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
            return TYPING_UPDATE
        case "Сотрудники":
            await update.message.reply_text("Введите ИД сотрудника: ")
            return TYPING_UPDATE
        case "Должности":
            await update.message.reply_text("Введите Название, Стаж: ")
            return TYPING_UPDATE
        case "Автомобили":
            await update.message.reply_text("Введите VIN: ")
            return TYPING_UPDATE
        case "Автосалоны":
            await update.message.reply_text("Введите ИД автосалона: ")
            return TYPING_UPDATE
        case "Поставщики":
            await update.message.reply_text("Введите ИД поставщика: ")
            return TYPING_UPDATE
        case "Заказы":
            await update.message.reply_text("Введите что-нибудь: ")
            return TYPING_UPDATE
    return ConversationHandler.END

async def typing_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["inputId"] = update.message.text
    table = context.user_data["table"]
    match table:
        case "Покупатели":
            await update.message.reply_text("Введите: ФИО, Телефон")
            return BUYERS
        case "Сотрудники":
            await update.message.reply_text("Введите: ФИО, Пропуски, Должность, Опыт")
            return WORKERS
        case "Автомобили":
            await update.message.reply_text("Введите: Марка, Название, Год, Цвет, Покраска, Кузов, Цена")
            return CARS
        case "Автосалоны":
            await update.message.reply_text("Введите: Название, Улица, Город, Рейтинг")
            return SHOPS
        case "Заказы":
            await update.message.reply_text("Введите: ИД магазина, ИД сотрудника, VIN, ИД покупателя, ИД поставщика, Адрес доставки, Итоговая цена")
            return ORDERS
        case "Должности":
            try:
                context.user_data["inputId"] = context.user_data["inputId"].split(", ")
            except:
                await update.message.reply_text("Ошибка ввода данных! Попробуйте снова")
                return TYPING_UPDATE
            await update.message.reply_text("Введите: Должность, Опыт, Зарплата")
            return JOBS
        case "Поставщики":
            await update.message.reply_text("Введите: Название, Страна, Регион, Город, Адрес")
            return DEALERS
    return ConversationHandler.END

async def update_buyers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    inputId = context.user_data["inputId"]
    try:
        fio, phone, = text.split(", ")
        logger.info("Got from user: %s, %s, ", fio, phone)
    except Exception as error:
        logger.info(error)
        await update.message.reply_text("Ошибка ввода данных! Попробуйте снова")
        return BUYERS
    conn = connectdb()
    with conn.cursor() as cur:
        try:
            cur.execute("UPDATE buyers SET fio = (%s), phone = (%s) WHERE buyerId = (%s)", (fio, phone, inputId))
        except psycopg2.errors.ForeignKeyViolation as e:
            logger.info(error)
        except psycopg2.errors.UniqueViolation as e:
            logger.info(error)
        conn.commit()
    conn.close()
    del context.user_data["inputId"]
    del context.user_data["table"]
    await update.message.reply_text("Готово!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def update_workers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    inputId = context.user_data["inputId"]
    try:
        fio, skips, position, experience = text.split(", ")
        logger.info("Got from user: %s, %s, %s, %s", fio, position, experience, skips)
        experience, skips = int(experience), int(skips)
    except Exception as error:
        logger.info(error)
        await update.message.reply_text("Ошибка ввода данных! Попробуйте снова")
        return WORKERS
    conn = connectdb()
    with conn.cursor() as cur:
        try:
            cur.execute("UPDATE workers SET FIO = (%s), position = (%s), experience = (%s), skips = (%s) WHERE workerId = (%s)", (fio, position, experience, skips, inputId))
        except psycopg2.errors.ForeignKeyViolation as e:
            logger.info(e)
        except psycopg2.errors.UniqueViolation as e:
            logger.info(e)
        conn.commit()
    conn.close()
    del context.user_data["inputId"]
    del context.user_data["table"]
    await update.message.reply_text("Готово!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def update_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    inputId = context.user_data["inputId"]
    try:
        position, experience, pay = text.split(", ")
        logger.info("Got from user: %s, %s, %s", position, experience, pay)
        experience, skips = int(experience), int(skips)
    except Exception as error:
        logger.info(error)
        await update.message.reply_text("Ошибка ввода данных! Попробуйте снова")
        return JOBS
    conn = connectdb()
    with conn.cursor() as cur:
        try:
            cur.execute("UPDATE positions SET position = (%s), experience = (%s), pay = (%s) WHERE position = (%s) and experience = (%s)", (position, experience, skips, inputId[0], inputId[1]))
        except psycopg2.errors.ForeignKeyViolation as e:
            logger.info(e)
        except psycopg2.errors.UniqueViolation as e:
            logger.info(e)
        conn.commit()
    conn.close()
    del context.user_data["inputId"]
    del context.user_data["table"]
    await update.message.reply_text("Готово!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
        
async def update_cars(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    inputId = context.user_data["inputId"]
    try:
        brand, name, year, colour, colourType, body, price = text.split(", ")
        logger.info("Got from user: %s, %s, %s, %s, %s", vin, brand, name, year, colour, colourType, body, price)
        vin, year, price = int(vin), int(year), int(price)
    except Exception as error:
        logger.info(error)
        await update.message.reply_text("Ошибка ввода данных! Попробуйте снова")
        return CARS
    conn = connectdb()
    with conn.cursor() as cur:
        try:
            cur.execute("UPDATE cars SET brand = (%s), name = (%s), year = (%s), colour = (%s), colourType = (%s), body = (%s), price = (%s) WHERE vin = (%S)", (brand, name, year, colour, colourType, body, price, inputId))
        except psycopg2.errors.ForeignKeyViolation as e:
            logger.info(e)
        except psycopg2.errors.UniqueViolation as e:
            logger.info(e)
        conn.commit()
    conn.close()
    del context.user_data["inputId"]
    del context.user_data["table"]
    await update.message.reply_text("Готово!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
    
async def update_shops(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    inputId = context.user_data["inputId"]
    try:
        name, address, city, rating = text.split(", ")
        logger.info("Got from user: %s, %s, %s, %s", name, address, city, rating)
    except Exception as error:
        logger.info(error)
        await update.message.reply_text("Ошибка ввода данных! Попробуйте снова")
        return SHOPS
    conn = connectdb()
    with conn.cursor() as cur:
        try:
            cur.execute("UPDATE shops SET name = (%s), address = (%s), city = (%s), rating = (%s) WHERE shopId = (%s)", (name, address, city, rating, inputId))
        except psycopg2.errors.ForeignKeyViolation as e:
            logger.info(e)
        except psycopg2.errors.UniqueViolation as e:
            logger.info(e)
        conn.commit()
    conn.close()
    del context.user_data["inputId"]
    del context.user_data["table"]
    await update.message.reply_text("Готово!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def update_dealers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    inputId = context.user_data["inputId"]
    try:
        name, country, region, city, address = text.split(", ")
        logger.info("Got from user: %s, %s, %s, %s, %s", name, country, region, city, address)
    except Exception as error:
        logger.info(error)
        await update.message.reply_text("Ошибка ввода данных! Попробуйте снова")
        return DEALERS
    conn = connectdb()
    with conn.cursor() as cur:
        try:
            cur.execute("UPDATE dealers SET name = (%s), country = (%s), region = (%s), city = (%s), address = (%s) WHERE dealerId = (%s)", (name, country, region, city, address, inputId))
        except psycopg2.errors.ForeignKeyViolation as e:
            logger.info(e)
        except psycopg2.errors.UniqueViolation as e:
            logger.info(e)
        conn.commit()
    conn.close()
    del context.user_data["inputId"]
    del context.user_data["table"]
    await update.message.reply_text("Готово!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def update_orders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    del context.user_data["inputId"]
    del context.user_data["table"]
    await update.message.reply_text("Класс, а теперь надо доделать это.")
    return ConversationHandler.END