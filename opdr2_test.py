from pymongo import MongoClient
import psycopg2
import regex

sql = ''
lst_category =['category',]
lst_sub_category = ['sub_category',]
lst_sub_sub_category =['sub_sub_category',]
lst_brand = ['brand',]


def check_exsisting_table_element(table:list, element:str,diction):
    global sql,lst_category,lst_sub_category,lst_sub_sub_categorylst_,brand

    try:
        if table[0] in diction:
            check_value_in_table = False
            for row in table:
                #print(row)
                if element == row:
                    check_value_in_table = True
                    break
            if not check_value_in_table:
                #print(f'{element} added')
                table.append(element)
                if table[0] == 'category':
                    sql +=(f"INSERT INTO category VALUES {element,0};")
                if table[0] == 'sub_category':
                    sql +=(f"INSERT INTO sub_category VALUES {element,0};")
                if table[0] == 'sub_sub_category':
                    sql +=(f"INSERT INTO sub_sub_category VALUES {element,0};")
                if table[0] == 'brand':
                    sql +=(f"INSERT INTO brand VALUES {element,0};")
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

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
    # product table
    try:

        local_product = item
        #print(local_product)
        id = (local_product['_id'])
        if  id.isdigit():
            id = int(id)
        else:
            #print(id)
            id = id.split('-')
            #print(id)
            id = id[0]
            #print(id)

        brand = Check_key_in_dict('brand', local_product)
        name = Check_key_in_dict('name', local_product)
        if "\'" in name:
            name = name.replace("\'", '')
        elif "'" in name:
            name = name.replace("'", "''")
        elif name == None:
            name = None
        category = Check_key_in_dict('category', local_product)
        gender = Check_key_in_dict('gender', local_product)
        discription = str(local_product['description'])
        if "\'" in discription:
            discription = discription.replace("\'",'')
        elif "'" in discription:
            discription = discription.replace("'","''")


        sub_category = Check_key_in_dict('sub_category',local_product)
        sub_sub_category = Check_key_in_dict('sub_sub_category', local_product)
        color = Check_key_in_dict('color', local_product)
        fast_mover = Check_key_in_dict('fast_mover', local_product)
        herhaalaankoop = Check_key_in_dict('herhaalaankoop', local_product)

        if '_preferences' in local_product:
            for item in local_product['_preferences']:
                if 'product_size' in item:
                    product_size = item.split(':')
                    sql +=(f"INSERT INTO product_size VALUES {product_size[1], 0};")
                if 'promos' in item:
                    promos = item.split(':')
                    sql +=(f"INSERT INTO promos VALUES {promos[1], 0};")

        else:
            product_size = None

        #print(category)
        if category != None: check_exsisting_table_element(lst_category,category,local_product)
        if sub_category != None: check_exsisting_table_element(lst_sub_category,sub_category,local_product)
        if sub_sub_category != None: check_exsisting_table_element(lst_sub_sub_category, sub_sub_category,local_product)
        if brand != None: check_exsisting_table_element(lst_brand, brand,local_product)
        sqlList = f"INSERT INTO product VALUES {id,name,brand,discription,gender,category,sub_category,sub_sub_category,color,fast_mover,herhaalaankoop,product_size}; "
        sqlList = sqlList.replace("None", "NULL")
        sql +=(sqlList)

    # price table
        selling_price = Check_key_in_dict('selling_price',local_product['price'])
        cost_price = Check_key_in_dict('cost_price',local_product['price'])
        deeplink = Check_key_in_dict('deeplink',local_product['price'])
        price_discription = Check_key_in_dict('description',local_product['price'])
        images = Check_key_in_dict('images',local_product['price'])
        label = Check_key_in_dict('label',local_product['price'])
        mrsp = Check_key_in_dict('mrsp',local_product['price'])
        price_properties = Check_key_in_dict('properties',local_product['price'])
        sqlList = f"INSERT INTO price VALUES {id, cost_price, deeplink, price_discription, selling_price, images, label, mrsp, name, price_properties};"
        sqlList = sqlList.replace("None", "NULL")
        sql +=(sqlList)



        properties = []
        for items in local_product['properties']:
            items.split(':')
            properties.append(items)
        for x in range(0,len(properties)):
            sqlList=f"INSERT INTO properties VALUES {id,properties[0],properties[1]};"
            sqlList = sqlList.replace("None", "NULL")
            sql +=(sqlList)


        is_active = Check_key_in_dict('is_active',local_product['sm'])
        last_updates = str(Check_key_in_dict('last_updated',local_product['sm']))
        rivals_updated = Check_key_in_dict('rivals_updated',local_product['sm'])
        sm_product_type = Check_key_in_dict('type',local_product['sm'])
        sqlList=f"INSERT INTO sm_product VALUES {id,is_active,last_updates,rivals_updated,sm_product_type};"
        sqlList = sqlList.replace("None", "NULL")
        sql +=(sqlList)

        if len(local_product['stock']) > 1:
            for item in local_product['stock']:
                stock_date = item['date']
                stock_level = item['stock_level']
                sqlList=f"INSERT INTO stock VALUES {id,stock_date,stock_level};"
                sqlList = sqlList.replace("None", "NULL")
                sql +=(sqlList)
        else:
            sqlList = f"INSERT INTO stock VALUES {id, None, None};"

            #con.commit()

    except IndexError:
        break
    except ValueError:
        pass
    except KeyError:
        pass
    except TypeError:
        pass
    except psycopg2.Error as e:
        # get error code
        error = e.pgcode
    finally:
        try:
            if i % 250 == 0:
                print(i)
            #print(sql)
            i +=1
            cur.execute(sql)
            con.commit()
            sql =''

        except psycopg2.Error as e:
            #print(e)
            sql =''
            i +=1
            cur.close
            con.close
            con = psycopg2.connect(
                host="localhost",
                database="opdracht2",
                user="postgres",
                password="kip12345",
            )
            cur = con.cursor()


#cur.execute(sql)
# con.commit()
cur.close()
con.close()
