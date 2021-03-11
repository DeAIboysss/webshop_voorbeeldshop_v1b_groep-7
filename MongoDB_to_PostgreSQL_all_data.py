import datetime
from pymongo import MongoClient
import psycopg2
import json

time0 = datetime.datetime.now()
client = MongoClient()
database = client.huwebshop

con = psycopg2.connect(
    host="localhost",
    database="huwebshop",
    user="postgres",
    password="admin",
)
cur = con.cursor()


def Check_key_in_dict(Key, Dict):
    if Key in Dict:
        return Dict[Key]
    else:
        return None


def get_product_data():
    prop_sql = []
    product_sql = []
    for local_product in database.products.find({}, {"_id": 1, "properties": 1, "name": 1, "price" : 1, "brand": 1, "sm": 1, "description": 1, "gender": 1, "category": 1,
                                                     "sub_category": 1, "sub_sub_category": 1, "fast_mover": 1,
                                                     "herhaalaankopen": 1,
                                                     "stock": 1, "_preferences": 1}):

        id = (local_product['_id'])
        brand = Check_key_in_dict('brand', local_product)
        name = Check_key_in_dict('name', local_product)
        if name != None:
            if "\'" in name:
                name = name.replace("\'", '')
            if "'" in name:
                name = name.replace("'", "''")
        category = Check_key_in_dict('category', local_product)
        gender = Check_key_in_dict('gender', local_product)
        description = Check_key_in_dict('description', local_product)
        description = str(description)
        if "\'" in description:
            description = description.replace("\'", '')
        elif "'" in description:
            description = description.replace("'", "''")


        sub_category = Check_key_in_dict('sub_category', local_product)
        sub_sub_category = Check_key_in_dict('sub_sub_category', local_product)
        color = Check_key_in_dict('color', local_product)
        fast_mover = Check_key_in_dict('fast_mover', local_product)
        herhaalaankopen = Check_key_in_dict('herhaalaankopen', local_product)


        if 'price' in local_product:
            selling_price = Check_key_in_dict('selling_price', local_product['price'])
        else:
            selling_price = None

        if 'sm' in local_product:
            is_active = Check_key_in_dict('is_active', local_product['sm'])
            sm_product_type = Check_key_in_dict('type', local_product['sm'])
        else:
            is_active = None
            sm_product_type = None

        if 'stock' in local_product:
            if len(local_product['stock']) > 1:
                stock_level = local_product['stock'][len(local_product['stock']) - 1]['stock_level']
            else:
                stock_level = None
        else:
            stock_level = None

        # sqlList = ;
        # sqlList = sqlList.replace("None", "NULL")
        product_sql.append((id, name, selling_price, brand, is_active, sm_product_type, description, gender,
                            category, sub_category, sub_sub_category, fast_mover, herhaalaankopen,
                            stock_level))
        if 'properties' in local_product:
            for key, value in local_product['properties'].items():
                if value != None and key != "klacht":
                    prop_sql.append((id, key, value))
    print('products and properties', datetime.datetime.now() - time0)
    return product_sql, prop_sql

def GetProfiledata():
    global time0
    i = 0
    profiles =[]
    previously_recommended = []
    similars =[]
    viewed_before=[]

    # time1 = datetime.datetime.now()
    # lasttime = datetime.datetime.now() -datetime.datetime.now()

    #while True  and i <itemindex:
    for profile in database.profiles.find({},{"_id":1,"order":1,"recommendations":1,"previously_recommended":1,"similars":1,"viewed_before":1}):

        local_profile =profile # db_profiles[i]

        #profiles table
        profile_id = str(local_profile["_id"])


        if 'order' in local_profile:
            if 'latest' in local_profile["order"]:
                latest = str(local_profile["order"]["latest"])
            else:
                latest = None
            if 'count' in local_profile["order"]:
                count = local_profile["order"]["count"]
            else:
                count = None
        else:
            latest = None
            count = None

        if 'recommendations' in local_profile:
            latest_activity = str(local_profile["recommendations"]["timestamp"])
            segment = local_profile["recommendations"]["segment"]
        else:
            latest_activity = None
            segment = None


        profiles.append((profile_id,latest_activity,latest,count,segment))

        if "previously_recommended" in local_profile:
            for product in local_profile["previously_recommended"]:
                previously_recommended.append((product, profile_id))
        if "recommendations" in local_profile:
            if "similars" in local_profile["recommendations"]:
                for product in local_profile["recommendations"]["similars"]:
                    similars.append((product, profile_id))

            if "viewed_before" in local_profile["recommendations"]:
                for product in local_profile["recommendations"]["viewed_before"]:
                    viewed_before.append((product, profile_id))
        i +=1


    print("profiles,previously_recommended,similars,viewed_before",datetime.datetime.now()-time0)

    return profiles,previously_recommended,similars,viewed_before


def get_sessions():
    '''
    Deze functie haalt alle data uit de collectie 'sessions' uit de MongoDB.
    De data wordt gefilterd foutieve waardes en zet deze om in het juiste format.
    Dit wordt vervolgens in een tuple gezet en toegevoegd aan een list per tabel.

    return:
        Drie lists met tuples.
    '''
    i = 0
    session_sql = []
    order_sql = []
    events_sql = []
    for local_sessions in database.sessions.find({},{"_id":1,"session_start":1,"session_end":1,"has_sale":1,"segment":1,"events":1,"order":1}):
        id = str(Check_key_in_dict('_id',local_sessions))
        session_start = str(Check_key_in_dict('session_start',local_sessions))
        session_end = str(Check_key_in_dict('session_end',local_sessions))
        has_sale = bool(Check_key_in_dict('has_sale',local_sessions))
        session_sql.append((id, session_start, session_end, has_sale, Check_key_in_dict('segment', local_sessions)))

        # events table:
        if 'events' in local_sessions:
            for event in local_sessions['events']:
                t = str(event['t'])
                source = event['source']
                action = event['action']
                events_sql.append((id, Check_key_in_dict('product', event), t, source, action,
                                   Check_key_in_dict('pagetype', event), Check_key_in_dict('time_on_page', event),
                                   Check_key_in_dict('click_count', event),Check_key_in_dict('elements_clicked',event)))

        # orders table:
        if 'order' in local_sessions and local_sessions['order'] != None:
            # print(f"order:\t{local_sessions['order']}")
            order = local_sessions['order']
            for product in order['products']:
                if product != None and not isinstance(product, str):
                        for key, value in product.items():
                            id_product = value
                            order_sql.append((id,id_product))
        # if i % 1000 == 0:
        #     print("sessions",i)
        # i+=1

    print("sessions, events and orders", datetime.datetime.now() - time0)
    return session_sql, events_sql, order_sql


product_sql, prop_sql = get_product_data()
profiles,previously_recommended,similars,viewed_before = GetProfiledata()
sessions, events, orders = get_sessions()
print("sql execute")

dict_values = {"INSERT INTO product VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);": product_sql,
               "INSERT INTO properties VALUES (%s,%s,%s);": prop_sql,
               "INSERT INTO profile VALUES (%s,%s,%s,%s,%s);": profiles,
               "INSERT INTO previously_recommended VALUES (%s,%s);": previously_recommended,
               "INSERT INTO similars VALUES (%s,%s);": similars,
               "INSERT INTO viewed_before VALUES (%s,%s);": viewed_before,
               "INSERT INTO sessions values(%s,%s,%s,%s,%s);": sessions,
               "INSERT INTO events values(%s,%s,%s,%s,%s,%s,%s,%s,%s);": events,
               "INSERT INTO orders values(%s,%s);": orders}

lst_insert_prints = []

for key, value in dict_values.items():
    cur.executemany(key, value)
    # con.commit()
    print(f"insert {value} done",datetime.datetime.now() - time0)

print('done')

con.commit()
cur.close()
con.close()
print(datetime.datetime.now() - time0)