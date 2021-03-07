from pymongo import MongoClient
import psycopg2
sql = []
lst_category =['category',]
lst_sub_category = ['sub_category',]
lst_sub_sub_category =['sub_sub_category',]
lst_brand = ['brand',]

lst_ids = []
# def check_exsisting_table_element(table:list, element:str,diction):
#     global sql,lst_category,lst_sub_category,lst_sub_sub_categorylst_,brand
#
#     try:
#         if table[0] in diction:
#             check_value_in_table = False
#             for row in table:
#                 #print(row)
#                 if element == row:
#                     check_value_in_table = True
#                     break
#             if not check_value_in_table:
#                 #print(f'{element} added')
#                 table.append(element)
#                 if table[0] == 'category':
#                     sql +=(f"INSERT INTO category VALUES {element,0};")
#                 if table[0] == 'sub_category':
#                     sql +=(f"INSERT INTO sub_category VALUES {element,0};")
#                 if table[0] == 'sub_sub_category':
#                     sql +=(f"INSERT INTO sub_sub_category VALUES {element,0};")
#                 if table[0] == 'brand':
#                     sql +=(f"INSERT INTO brand VALUES {element,0};")
#     except (Exception, psycopg2.Error) as error:
#         print("Error while fetching data from PostgreSQL", error)

def Check_key_in_dict(Key,Dict):
    if Key in Dict:
        return Dict[Key]
    else:
        return None

client = MongoClient()
database = client.huwebshop

db_products = database.products.find()
con = psycopg2.connect(
    host="localhost",
    database="opdracht2",
    user="postgres",
    password="kip12345",
)
i = 0
cur = con.cursor()


for item in db_products:
    local_product = item
    id = (local_product['_id'])
    double_ID = False

    if id.isdigit():
        id = int(id)
    else:
        id = id.split('-')
        id = id[0]
    for idees in lst_ids:
        if idees == id:
            double_ID = True
            break
    if double_ID == False:
        lst_ids.append(id)
        brand = Check_key_in_dict('brand', local_product)
        name = Check_key_in_dict('name', local_product)
        if name != None:
            if "\'" in name:
                name = name.replace("\'", '')
            if "'" in name:
                name = name.replace("'", "''")
        category = Check_key_in_dict('category', local_product)
        gender = Check_key_in_dict('gender', local_product)
        discription = Check_key_in_dict('description',local_product)
        discription = str(discription)
        if "\'" in discription:
            discription = discription.replace("\'",'')
        elif "'" in discription:
            discription = discription.replace("'","''")


        sub_category = Check_key_in_dict('sub_category',local_product)
        sub_sub_category = Check_key_in_dict('sub_sub_category', local_product)
        color = Check_key_in_dict('color', local_product)
        fast_mover = Check_key_in_dict('fast_mover', local_product)
        herhaalaankoop = Check_key_in_dict('herhaalaankoop', local_product)
        product_size = None
        promos = None

        if '_preferences' in local_product:
            for item in local_product['_preferences']:
                if 'product_size' in item:
                    product_size = item.split(':')
                    #sql +=(f"INSERT INTO product_size VALUES {product_size[1], 0};")
                if 'promos' in item:
                    promos = item.split(':')
                    #sql +=(f"INSERT INTO promos VALUES {promos[1], 0};")

        else:
            product_size = None
            promos = None
        if 'price' in local_product:
            selling_price = Check_key_in_dict('selling_price', local_product['price'])
            cost_price = Check_key_in_dict('cost_price', local_product['price'])
        else:
            selling_price = None
            cost_price = None

        if 'sm' in local_product:
            is_active = Check_key_in_dict('is_active', local_product['sm'])
            sm_product_type = Check_key_in_dict('type', local_product['sm'])
        else:
            is_active = None
            sm_product_type =  None

        if 'stock' in local_product:
            if len(local_product['stock']) > 1:
                stock_level = local_product['stock'][len(local_product['stock'])-1]['stock_level']
            else:
                stock_level = None
        else:
            stock_level = None

        sqlList = f"INSERT INTO product VALUES {id,name,cost_price,selling_price,brand,is_active,sm_product_type,discription,gender,category,sub_category,sub_sub_category,fast_mover,herhaalaankoop,product_size,promos,stock_level}; "
        sqlList = sqlList.replace("None", "NULL")
        sql.append(sqlList)
        properties = []
        # if 'properties' in local_product:
        #     for items in local_product['properties']:
        #         items.split(':')
        #         properties.append(items)
        #     for x in range(0,len(properties)):
        #         sqlList=f"INSERT INTO properties VALUES {id,properties[0],properties[1]};"
        #         sqlList = sqlList.replace("None", "NULL")
        #         sql.append(sqlList)

    # if i % 1000 == 0:
    #     print(i,id)
            #print(sql)
    i +=1

i = 0
for item in sql:
    try:
        # if i % 1000 == 0:
        #     print(i)
        #print(item)
        cur.execute(item)
        con.commit()
        i+=1
    except psycopg2.Error as e:
        cur.close()
        con.close()
        con = psycopg2.connect(
            host="localhost",
            database="opdracht2",
            user="postgres",
            password="kip12345",
        )
        cur = con.cursor()

        print(e)
        #pass

cur.close()
con.close()
