import os
from dotenv import load_dotenv

import psycopg2

load_dotenv()

def createdb(): # Создание новой базы данных
    conn = psycopg2.connect(
    dbname="postgres",
    user=os.getenv("DATABASE_USERNAME"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_IP"),
    port=os.getenv("DATABASE_PORT")
    )
    conn.autocommit = True
    with conn.cursor() as cur:
        try:
            cur.execute("CREATE DATABASE tgdb")
        except psycopg2.errors.DuplicateDatabase as e:
            print("Database already exists")
    conn.close()

def removedb(): # Удаление базы данных
    conn = psycopg2.connect(
    dbname="postgres",
    user=os.getenv("DATABASE_USERNAME"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_IP"),
    port=os.getenv("DATABASE_PORT")
    )
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("DROP DATABASE IF EXISTS tgdb")
    conn.close()
    
def create_tables(conn): # Создание таблиц
    with conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE keys_table
            (workerId INTEGER,
            vin INTEGER,
            buyerId INTEGER,
            deliveryAddr VARCHAR(100),
            dealerId INTEGER)
        ''')
        cur.execute('''
            CREATE TABLE total_prices
            (shopId INTEGER,
            vin INTEGER,
            buyerId INTEGER,
            deliveryAddr VARCHAR(100),
            totalPrice INTEGER)
        ''')
        cur.execute('''
            CREATE TABLE shops
            (shopId INTEGER,
            name VARCHAR(100),
            address VARCHAR(100),
            city VARCHAR(100),
            rating INTEGER)
        ''')
        cur.execute('''
            CREATE TABLE workers
            (workerId INTEGER,
            FIO VARCHAR(100),
            position VARCHAR(100),
            experience INTEGER,
            skips INTEGER)
        ''')
        cur.execute('''
            CREATE TABLE positions
            (position VARCHAR(100),
            pay INTEGER)
        ''')
        cur.execute('''
            CREATE TABLE cars
            (vin INTEGER,
            brand VARCHAR(100),
            name VARCHAR(100),
            year INTEGER,
            colour VARCHAR(100),
            colourType VARCHAR(100),
            body VARCHAR(100),
            price INTEGER)
        ''')
        cur.execute('''
            CREATE TABLE dealers
            (dealerId INTEGER,
            name VARCHAR(100),
            country VARCHAR(100),
            region INTEGER,
            city VARCHAR(100),
            address VARCHAR(100))
        ''')
        cur.execute('''
            CREATE TABLE buyers
            (buyerId INTEGER,
            FIO VARCHAR(100),
            phone VARCHAR(100))
        ''')
        cur.execute('''
            CREATE TABLE discountCards
            (buyerId INTEGER,
            shopId INTEGER,
            type VARCHAR(100))
        ''')

def main():
    removedb()
    createdb()
    
    conn = psycopg2.connect(
    dbname=os.getenv("DATABASE_NAME"),
    user=os.getenv("DATABASE_USERNAME"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_IP"),
    port=os.getenv("DATABASE_PORT")
    )
    create_tables(conn)
    conn.close()

if __name__ == "__main__":
    main()