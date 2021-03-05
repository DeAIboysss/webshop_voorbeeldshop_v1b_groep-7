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

def check_if_column_exists(column, sessions):
    #print(column)
    #print(sessions)
    if column == None:
        pass
    if column in sessions:
        #print(column)
        return sessions[column]
    return None


while True and i < 100000:
    try:
        #sessions table:
        local_sessions = db_sessions[i]
        id = str(local_sessions['_id'])
        session_start = str(local_sessions['session_start'])
        session_end = str(local_sessions['session_end'])
        has_sale = bool(local_sessions['has_sale'])
        cg_treated = bool(local_sessions['cg_treated'])
        tg_treated = bool(local_sessions['tg_treated'])

        sql = f"INSERT INTO sessions VALUES {id, None, None, session_start, session_end, has_sale, cg_treated, tg_treated, check_if_column_exists('segment', local_sessions), check_if_column_exists('clean_cg_tg', local_sessions)};"
        sql = sql.replace("None", "NULL")
        cur.execute(sql)

        #events table:
        for event in local_sessions['events']:
            t = str(event['t'])
            source = event['source']
            action = event['action']

            sql_event = f"INSERT INTO events VALUES {id, t, source, action, check_if_column_exists('pagetype', event), check_if_column_exists('product', event), check_if_column_exists('time_on_page', event), check_if_column_exists('max_time_inactive', event), check_if_column_exists('click_count', event), check_if_column_exists('elements_clicked', event), check_if_column_exists('scrolls_down', event), check_if_column_exists('scrolls_up', event)};"
            sql_event = sql_event.replace("None", "NULL")
            cur.execute(sql_event)

        #sources tables:                                # <= NOTE: id is int8 and not SERIAL for the time being. also deleted FK in DDL.
        if 'sources' in local_sessions:
            if len(local_sessions['sources']) > 0:

                for source in local_sessions['sources']:
                    # print(source)
                    # t = str(source['t'])

                    sql_sources = f"INSERT INTO sources VALUES {None, check_if_column_exists('full_url', source), check_if_column_exists('netloc', source), None, t};"
                    sql_sources = sql_sources.replace("None", "NULL")
                    cur.execute(sql_sources)


    except IndexError:
        print('IndexError')
        break
    except ValueError:
        print('ValueError')
        pass
    # except KeyError:
    #     print('KeyError')
    #     pass
    # except psycopg2.Error:
    #     print('psycopg2.Error')
    #     pass
    finally:
        #print(id,"succes")
        print("succes")

        con.commit()
        i += 1


cur.close()
con.close()