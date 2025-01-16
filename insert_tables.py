import psycopg2

def insert_workers(conn):
    fio = input("Input FIO: ")
    position = input("Input position: ")
    experience = input("Input exp: ")
    skips = input("Input skips: ")
    with conn.cursor() as cur:
        try:
            cur.execute("INSERT INTO workers VALUES (DEFAULT, %s, %s, %s, %s)", (fio, position, experience, skips))
        except psycopg2.errors.ForeignKeyViolation as e:
            pay = input("Input pay: ")
            cur.execute("INSERT INTO positions VALUES (DEFAULT, %s, %s, %s, %s)", (position, experience, pay))
            cur.execute("INSERT INTO workers VALUES (DEFAULT, %s, %s, %s, %s)", (fio, position, experience, skips))
        conn.commit()
        
def insert_cars(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM cars ORDER BY cars.vin;")
        conn.commit()
        
def insert_shops(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM shops ORDER BY shops.shopId;")
        conn.commit()
        
def insert_orders(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM keys_table;")
        conn.commit()
