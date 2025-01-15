import psycopg2

def create_tables(conn): # Создание таблиц
    with conn.cursor() as cur:
        #Автосалоны
        cur.execute('''
            CREATE TABLE shops
            (shopId INTEGER GENERATED ALWAYS AS IDENTITY constraint shop_pk primary key,
            name VARCHAR(100) not null,
            address VARCHAR(100) not null,
            city VARCHAR(100) not null,
            rating INTEGER not null
            )
        ''')
        #Должности
        cur.execute('''
            CREATE TABLE positions
            (position VARCHAR(100) not null,
            experience INTEGER not null,
            pay INTEGER not null,
            PRIMARY KEY (position, experience)
            )
        ''')
        #Сотрудники
        cur.execute('''
            CREATE TABLE workers
            (workerId INTEGER GENERATED ALWAYS AS IDENTITY constraint worker_pk primary key,
            FIO VARCHAR(100) not null,
            position VARCHAR(100) not null,
            experience INTEGER not null,
            skips INTEGER not null,
            FOREIGN KEY (position, experience) references positions on update cascade on delete cascade
            )
        ''')
        #Автомобили
        cur.execute('''
            CREATE TABLE cars
            (vin INTEGER not null constraint vin_pk primary key,
            brand VARCHAR(100) not null,
            name VARCHAR(100) not null,
            year INTEGER not null,
            colour VARCHAR(100) not null,
            colourType VARCHAR(100) not null,
            body VARCHAR(100) not null,
            price INTEGER not null
            )
        ''')
        #Поставщики
        cur.execute('''
            CREATE TABLE dealers
            (dealerId INTEGER GENERATED ALWAYS AS IDENTITY constraint dealer_pk primary key,
            name VARCHAR(100) not null,
            country VARCHAR(100) not null,
            region VARCHAR(100) not null,
            city VARCHAR(100) not null,
            address VARCHAR(100) not null
            )
        ''')
        #Покупатели
        cur.execute('''
            CREATE TABLE buyers
            (buyerId INTEGER GENERATED ALWAYS AS IDENTITY constraint buyer_pk primary key,
            FIO VARCHAR(100) not null,
            phone VARCHAR(100) not null
            )
        ''')
        #Скидочные карты
        cur.execute('''
            CREATE TABLE discount_cards
            (buyerId INTEGER not null constraint buyer_cards_fk references buyers on update cascade on delete cascade,
            shopId INTEGER not null constraint shop_cards_fk references shops on update cascade on delete cascade,
            type VARCHAR(100) not null
            )
        ''')
        #Итоговые цены
        cur.execute('''
            CREATE TABLE total_prices
            (shopId INTEGER not null constraint shop_tp_fk references shops on update cascade on delete cascade,
            vin INTEGER not null constraint vin_tp_fk references cars on update cascade on delete cascade,
            buyerId INTEGER not null constraint buyer_tp_fk references buyers on update cascade on delete cascade,
            deliveryAddr VARCHAR(100) not null constraint addr_pk primary key,
            dealerId INTEGER not null constraint dealer_tp_fk references dealers on update cascade on delete cascade,
            totalPrice INTEGER not null
            )
        ''')
        #Покупки
        cur.execute('''
            CREATE TABLE keys_table
            (shopId INTEGER not null constraint shop_kt_fk references shops on update cascade on delete cascade,
            workerId INTEGER not null constraint worker_kt_fk references workers on update cascade on delete cascade,
            vin INTEGER not null constraint vin_kt_fk references cars on update cascade on delete cascade,
            buyerId INTEGER not null constraint buyer_kt_fk references buyers on update cascade on delete cascade,
            deliveryAddr VARCHAR(100) not null constraint addr_kt_fk references total_prices on update cascade on delete cascade,
            dealerId INTEGER not null constraint dealer_kt_fk references dealers on update cascade on delete cascade
            )
        ''')
        conn.commit()
        
def fill_tables(conn): # Заполнение таблиц
    with conn.cursor() as cur:
        cur.execute('''
                INSERT INTO shops VALUES
                (DEFAULT, 'Патриот', 'ул. Букирева 23', 'Томск', 4)
        ''')
        cur.execute('''
                INSERT INTO cars VALUES
                (1, 'Mazda', 'Super', 2020, 'Белый', 'Глянцевый', 'Седан', 1000000)
        ''')
        cur.execute('''
                INSERT INTO positions VALUES
                ('Менеджер', 2, 30000)
        ''')
        cur.execute('''
                INSERT INTO workers VALUES
                (DEFAULT, 'Вяткин Данил Андреевич', 'Менеджер', 2, 1)
        ''')
        cur.execute('''
                INSERT INTO dealers VALUES
                (DEFAULT, 'Masta cars', 'США', 'Нью-Йорк', 'Нью-Йорк', 'Бокстрит 35')
        ''')
        cur.execute('''
                INSERT INTO buyers VALUES
                (DEFAULT, 'Жданов Андрей Игнатин', '7(1086)518-99-66')
        ''')
        cur.execute('''
                INSERT INTO discount_cards VALUES
                (1, 1, 'Золотая')
        ''')
        cur.execute('''
                INSERT INTO total_prices VALUES
                (1, 1, 1, 'ул. Карпинского 45', 1, 1230000)
        ''')
        cur.execute('''
                INSERT INTO keys_table VALUES
                (1, 1, 1, 1, 'ул. Карпинского 45', 1)
        ''')
        conn.commit()