import psycopg2
from dbmanage import connectdb

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