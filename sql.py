import os
from dotenv import load_dotenv

from template import create_tables, fill_tables

import psycopg2
from psycopg2 import sql

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
            query = "CREATE DATABASE {} ;"
            dbname = os.getenv("DATABASE_NAME")
            cur.execute(sql.SQL(query).format(
                sql.Identifier(dbname)))
        except psycopg2.errors.DuplicateDatabase as e:
            print("Database already exists")
            print(e)
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
    fill_tables(conn)
    conn.close()

if __name__ == "__main__":
    main()