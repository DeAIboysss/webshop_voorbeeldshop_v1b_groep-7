from pymongo import MongoClient
import psycopg2

import itertools as it
from collections import Counter

client = MongoClient()
database = client.huwebshop

db_products = database.products.find()
db_sessions = database.sessions.find()
con = psycopg2.connect(
    host="localhost",
    database="huwebshop",
    user="postgres",
    password="admin",
)
i = 0
cur = con.cursor()

#empty strings for queries to fill:
sql_sessions = []
sql_events = []
sql_orders = []


def check_if_column_exists(column, sessions):
    if column == None:
        pass
    if column in sessions:
        return sessions[column]
    return None


while True and i < 1500:
    try:
        # sessions table:
        local_sessions = db_sessions[i]
        id = str(local_sessions['_id'])
        session_start = str(local_sessions['session_start'])
        session_end = str(local_sessions['session_end'])
        has_sale = bool(local_sessions['has_sale'])

        sql = f"INSERT INTO sessions VALUES {id,session_start, session_end, has_sale, check_if_column_exists('segment', local_sessions)};"
        sql = sql.replace("None", "NULL")
        cur.execute(sql)

        # events table:
        for event in local_sessions['events']:
            t = str(event['t'])
            source = event['source']
            action = event['action']

            # sql_event = f"INSERT INTO events VALUES {id, PRODUCTID HIER!!!, t, source, action, check_if_column_exists('pagetype', event), check_if_column_exists('time_on_page', event), check_if_column_exists('click_count', event)};"
            sql_event = f"INSERT INTO events VALUES {id, check_if_column_exists('product', event), t, source, action, check_if_column_exists('pagetype', event), check_if_column_exists('time_on_page', event), check_if_column_exists('click_count', event)};"
            sql_event = sql_event.replace("None", "NULL")
            cur.execute(sql_event)

        # orders table:
        if 'order' in local_sessions and local_sessions['order'] != None:
            #print(f"order:\t{local_sessions['order']}")
            order = local_sessions['order']

            for products, ids in order.items():
                if ids != None:
                    for prod in ids:
                        for key, value in prod.items():
                            id_product = value

                            sql_orders = f"INSERT INTO orders VALUES {None, id_product, id};"
                            sql_orders = sql_orders.replace("None", "NULL")
                            cur.execute(sql_orders)


    except IndexError:
        print('IndexError')
        break
    except ValueError:
        print('ValueError')
        pass
    except KeyError:
        print('KeyError')
        pass
    except psycopg2.Error:
        print('psycopg2.Error')
        pass
    finally:
        # print(id,"succes")
        if i % 100 == 0:
            print("succes") # <= print every 100 succesvolle lines, is faster.

        con.commit()
        i += 1

cur.close()
con.close()