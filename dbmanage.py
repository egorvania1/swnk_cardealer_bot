import os
from dotenv import load_dotenv

import psycopg2

load_dotenv()

def connectdb():
    conn = psycopg2.connect(
    dbname=os.getenv("DATABASE_NAME"),
    user=os.getenv("DATABASE_USERNAME"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_IP"),
    port=os.getenv("DATABASE_PORT")
    )
    conn.set_client_encoding('UTF8')
    return conn

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
        try:
            query = "DROP DATABASE {} ;"
            dbname = os.getenv("DATABASE_NAME")
            cur.execute(sql.SQL(query).format(
                sql.Identifier(dbname)))
        except psycopg2.errors.InvalidCatalogName as e:
            print(e)
    conn.close()