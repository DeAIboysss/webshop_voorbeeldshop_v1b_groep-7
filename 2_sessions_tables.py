from pymongo import MongoClient
import psycopg2

client = MongoClient()
database = client.huwebshop

# db_products = database.products.find()
db_sessions = database.sessions.find()
con = psycopg2.connect(
    host="localhost",
    database="huwebshop",
    user="postgres",
    password="admin",
)
i = 0
cur = con.cursor()


while True and i < 100:
    try:
        #sessions table:
        local_sessions = db_sessions[i]
        id = str(local_sessions['_id'])
        session_start = str(local_sessions['session_start'])
        session_end = str(local_sessions['session_end'])
        has_sale = bool(local_sessions['has_sale'])
        cg_treated = bool(local_sessions['cg_treated'])
        tg_treated = bool(local_sessions['tg_treated'])

        # print(session_start)
        # print(type(session_start))

        if 'segment' in local_sessions and 'clean_cg_tg' in local_sessions:
            segment = local_sessions['segment']
            clean_cg_tg = local_sessions['clean_cg_tg']
            sql = f"INSERT INTO sessions VALUES {id, None, None, session_start, session_end, has_sale, cg_treated, tg_treated, segment, clean_cg_tg};"
            sql = sql.replace("None", "NULL")
            cur.execute(sql)
        elif 'segment' in local_sessions and 'clean_cg_tg' not in local_sessions:
            segment = local_sessions['segment']
            sql = f"INSERT INTO sessions VALUES {id, None, None, session_start, session_end, has_sale, cg_treated, tg_treated, segment, None};"
            sql = sql.replace("None", "NULL")
            cur.execute(sql)
        elif 'segment' not in local_sessions and 'clean_cg_tg' in local_sessions:
            clean_cg_tg = local_sessions['clean_cg_tg']
            sql = f"INSERT INTO sessions VALUES {id, None, None, session_start, session_end, has_sale, cg_treated, tg_treated, None, clean_cg_tg};"
            sql = sql.replace("None", "NULL")
            cur.execute(sql)
        else:
            segment = local_sessions['segment']
            clean_cg_tg = local_sessions['clean_cg_tg']
            sql = f"INSERT INTO sessions VALUES {id, None, None, session_start, session_end, has_sale, cg_treated, tg_treated, None, None};"
            sql = sql.replace("None", "NULL")
            cur.execute(sql)


        # #events table:
        # #is bestaat al als "id"
        # for event in local_sessions['events']: # <= evt afvangen als er geen event is!
        #     t = str(event['t'])
        #     source = event['source']
        #     action = event['action']
        #     pagetype = event['pagetype']
        #     product = event['product']
        #
        #     time_on_page = str(event['time_on_page'])               #check if exists
        #     max_time_inactive = str(event['max_time_inactive'])     #check if exists
        #     click_count = event['click_count']                      #check if exists
        #     elements_clicked = event['elements_clicked']            #check if exists
        #     scrolls_down = event['scrolls_down']                    #check if exists
        #     scrolls_up = event['scrolls_up']                        #check if exists
        #
        #
        #     if 'time_on_page' in local_sessions['events']:





        #     cur.execute(f"INSERT INTO events VALUES {id, t, source, action , pagetype, product, time_on_page, max_time_inactive, click_count, elements_clicked, scrolls_up, scrolls_down};")
        # con.commit()





        # #sources table:
        # #id bestaat al als "sourcesid"
        # for source in local_sessions['sources']:
        #     full_url = source['full_url']
        #     netloc = source['netloc']
        #     params = source['params']
        #     t = source['t']
        #
        #     cur.execute(f"INSERT INTO sources VALUES {sourcesid, full_url, netloc, params , t};")
        # con.commit()
        #
        # #user_agent table:
        # cur.execute(f"INSERT INTO user_agent VALUES {id};")
        # con.commit()
        #
        # #os table:
        # #user_agentsessionsid bestaat al als "id"
        # family = local_sessions['user_agent']['os']['family']
        # version_string = local_sessions['user_agent']['os']['version_string']
        #
        # cur.execute(f"INSERT INTO os VALUES {id, family, version_string};")
        # con.commit()
        #
        # #browser table:
        # family_1 = local_sessions['user_agents']['browser']['family']
        # version_string_1 = local_sessions['user_agents']['browser']['version_string']
        #
        # cur.execute(f"INSERT INTO browser VALUES {id, family_1, version_string_1};")
        # con.commit()
        #
        # #device table:
        # family_2 = local_sessions['user_agents']['device']['family']
        # brand = local_sessions['user_agents']['device']['brand']
        # model = local_sessions['user_agents']['device']['model']
        #
        # cur.execute(f"INSERT INTO device VALUES {id, family_2, brand, model};")
        # con.commit()
        #
        # #table order:
        # #id bestaat al als "orderid"
        # payment_method = local_sessions['order']['payment_method']
        # total = local_sessions['order']['total']
        # taxes = local_sessions['order']['taxes']
        #
        # cur.execute(f"INSERT INTO device VALUES {orderid, payment_method, total, taxes};")
        # con.commit()


    except IndexError:
        print('IndexError')
        break
    except ValueError:
        print('ValueError')
        pass
    except KeyError:
        print('KeyError')
        pass
    # except psycopg2.Error:
    #     print('psycopg2.Error')
    #     pass
    finally:
        print(id,"succes")

        con.commit()
        i += 1


cur.close()
con.close()