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
        
def insert_buyers(conn):
    fio = input("Input FIO: ")
    phone = input("Input phone: ")
    with conn.cursor() as cur:
        try:
            cur.execute("INSERT INTO buyers VALUES (DEFAULT, %s, %s)", (fio, phone))
        except psycopg2.errors.ForeignKeyViolation as e:
            print(e)
        conn.commit()
        
def insert_dealers(conn):
    name = input("Input name: ")
    country = input("Input country: ")
    region = input("Input region: ")
    city = input("Input city: ")
    address = input("Input address: ")
    with conn.cursor() as cur:
        try:
            cur.execute("INSERT INTO buyers VALUES (DEFAULT, %s, %s, %s, %s, %s)", (name, country, region, city, address))
        except psycopg2.errors.ForeignKeyViolation as e:
            print(e)
        conn.commit()
        
def insert_cars(conn):
    vin = input("Input vin: ")
    brand = input("Input brand: ")
    name = input("Input name: ")
    year = input("Input year: ")
    colour = input("Input colour: ")
    colourType = input("Input colourType: ")
    body = input("Input body: ")
    price = input("Input price: ")
    with conn.cursor() as cur:
        try:
            cur.execute("INSERT INTO cars VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (vin, brand, name, year, colour, colourType, doby, price))
        except psycopg2.errors.ForeignKeyViolation as e:
            print(e)
        conn.commit()
        
def insert_shops(conn):
    name = input("Input name: ")
    address = input("Input address: ")
    city = input("Input city: ")
    rating = input("Input rating: ")
    with conn.cursor() as cur:
        try:
            cur.execute("INSERT INTO shops VALUES (DEFAULT, %s, %s, %s, %s)", (name, address, city, rating))
        except psycopg2.errors.ForeignKeyViolation as e:
            print(e)
        conn.commit()
        
def insert_orders(conn):
    shopId = input("Input shopId: ")
    workerId = input("Input workerId: ")
    vin = input("Input vin: ")
    buyerId = input("Input buyerId: ")
    deliveryaddr = input("Input deliveryAddr: ")
    dealerid = input("Input dealerid: ")
    totalprice = input("Input totalprice: ")
    with conn.cursor() as cur:
        try:
            cur.execute("INSERT INTO shops VALUES (DEFAULT, %s, %s, %s, %s)", (name, address, city, rating))
        except psycopg2.errors.ForeignKeyViolation as e:
            print(e)
