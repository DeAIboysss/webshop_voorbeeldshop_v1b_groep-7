from pymongo import MongoClient
import psycopg2

client = MongoClient()
database = client.huwebshop

# db_products = database.products.find()
db_sessions = database.sessions.find()
con = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="admin",
)
i = 0
cur = con.cursor()

while True:
    try:
        #sessions table:
        local_sessions = db_sessions[i]
        id = str(local_sessions['_id'])
        orderid = local_sessions['order']
        sourcesid = local_sessions['sources']
        session_start = local_sessions['session_start']
        session_end = local_sessions['session_end']
        has_sale = bool(local_sessions['has_sale'])
        cg_treated = bool(local_sessions['cg_treated'])
        tg_treated = bool(local_sessions['tg_treated'])
        segment = local_sessions['segment']
        clean_cg_tg = local_sessions['clean_cg_tg']

        # cur.execute(f"INSERT INTO sessions VALUES {id, orderid, sourcesid, session_start,session_end, has_sale, cg_treated, tg_treated, segment, clean_cg_tg};")
        # con.commit()

        #events table:
        #is bestaat al als "id"
        for event in local_sessions['events']: # <= evt afvangen als er geen event is!
            t = event['t']
            source = event['source']
            action = event['acion']
            pagetype = event['pagetype']
            product = event['product']
            time_on_page = float(event['time_on_page'])
            max_time_inactive = float(event['max_time_inactive'])
            click_count = int(event['click_count'])
            elements_clicked = int(event['elements_clicked'])
            scrolls_down = int(event['scrolls_down'])
            scrolls_up = int(event['scrolls_up'])

        #     cur.execute(f"INSERT INTO events VALUES {id, t, source, action , pagetype, product, time_on_page, max_time_inactive, click_count, elements_clicked, scrolls_up, scrolls_down};")
        # con.commit()

        #sources table:
        #id bestaat al als "sourcesid"
        for source in local_sessions['sources']:
            full_url = source['full_url']
            netloc = source['netloc']
            params = source['params']
            t = source['t']

        #     cur.execute(f"INSERT INTO sources VALUES {sourcesid, full_url, netloc, params , t};")
        # con.commit()

        #user_agent table:
        # cur.execute(f"INSERT INTO user_agent VALUES {id};")
        # con.commit()

        #os table:
        #user_agentsessionsid bestaat al als "id"
        family = local_sessions['user_agent']['os']['family']
        version_string = local_sessions['user_agent']['os']['version_string']

        # cur.execute(f"INSERT INTO os VALUES {id, family, version_string};")
        # con.commit()

        #browser table:
        family_1 = local_sessions['user_agents']['browser']['family']
        version_string_1 = local_sessions['user_agents']['browser']['version_string']

        # cur.execute(f"INSERT INTO browser VALUES {id, family_1, version_string_1};")
        # con.commit()

        #device table:
        family_2 = local_sessions['user_agents']['device']['family']
        brand = local_sessions['user_agents']['device']['brand']
        model = local_sessions['user_agents']['device']['model']

        # cur.execute(f"INSERT INTO device VALUES {id, family_2, brand, model};")
        # con.commit()

        #table order:
        #id bestaat al als "orderid"
        payment_method = local_sessions['order']['payment_method']
        total = local_sessions['order']['total']
        taxes = local_sessions['order']['taxes']

        # cur.execute(f"INSERT INTO device VALUES {orderid, payment_method, total, taxes};")
        # con.commit()


    except IndexError:
        break
    except ValueError:
        pass
    except KeyError:
        pass
    except psycopg2.Error:
        pass
    finally:
        #print(id,"succes")

        con.commit()
        i += 1


cur.close()
con.close()