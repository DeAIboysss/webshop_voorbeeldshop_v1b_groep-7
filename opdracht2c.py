from pymongo import MongoClient
import psycopg2
import regex

sql = ''


def check_exsisting_table_element(table, element):

        postgreSQL_select_Query = f"select * from {table}"

        cur.execute(postgreSQL_select_Query)
        #print("Selecting rows from mobile table using cursor.fetchall")
        table_records = cur.fetchall()
        check_value_in_table = False
        for row in table_records:
            #print(row)
            if element in row:
                check_value_in_table = True
        if not check_value_in_table:

            #print(f'{element} added')
            cur.execute(f"INSERT INTO {table} VALUES {element, 0};")


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


while True:
    # product table
    #try:

        local_product = db_products[i]
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
                    cur.execute(f"INSERT INTO product_size VALUES {product_size[1], 0};")
                if 'promos' in item:
                    promos = item.split(':')
                    cur.execute(f"INSERT INTO promos VALUES {promos[1], 0};")

        else:
            product_size = None

        #print(category)
        check_exsisting_table_element('category',category)
        check_exsisting_table_element('sub_category',sub_category)
        check_exsisting_table_element('sub_sub_category', sub_sub_category)
        check_exsisting_table_element('brand', brand)
        # try:
        #     postgreSQL_select_Query = f"select * from product"
        #
        #     cur.execute(postgreSQL_select_Query)
        #     #print("Selecting rows from mobile table using cursor.fetchall")
        #     table_records = cur.fetchall()
        #     check_value_in_table = False
        #     for row in table_records:
        #         #print(row)
        #         if id in row:
        #             check_value_in_table = True


        # except (Exception, psycopg2.Error) as error:
        #     print("Error while fetching data from PostgreSQL", error)
        #if not check_value_in_table:
            #print(f'{id} added')
        sqlList = f"INSERT INTO product VALUES {id,name,brand,discription,gender,category,sub_category,sub_sub_category,color,fast_mover,herhaalaankoop,product_size}; "
        sqlList = sqlList.replace("None", "NULL")
        cur.execute(sqlList)

    # price table

        #print(local_product['price'])
        selling_price = Check_key_in_dict('selling_price',local_product['price'])
        cost_price = Check_key_in_dict('cost_price',local_product['price'])
        deeplink = Check_key_in_dict('deeplink',local_product['price'])
        price_discription = Check_key_in_dict('description',local_product['price'])
        images = Check_key_in_dict('images',local_product['price'])
        label = Check_key_in_dict('label',local_product['price'])
        mrsp = Check_key_in_dict('mrsp',local_product['price'])
        price_properties = Check_key_in_dict('properties',local_product['price'])

        try:
            postgreSQL_select_Query = f"select * from price"

            cur.execute(postgreSQL_select_Query)
            #print("Selecting rows from mobile table using cursor.fetchall")
            table_records = cur.fetchall()
            check_value_in_table = False
            for row in table_records:
                #print(row)
                if id in row:
                    check_value_in_table = True


        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
        if not check_value_in_table:
            #print(f'{id} added')
            sqlList = f"INSERT INTO price VALUES {id, cost_price, deeplink, price_discription, selling_price, images, label, mrsp, name, price_properties};"
            sqlList = sqlList.replace("None", "NULL")
            cur.execute(sqlList)



        properties = []
        for items in local_product['properties']:
            items.split(':')
            properties.append(items)
        for x in range(0,len(properties)):

            try:
                postgreSQL_select_Query = f"select * from properties"

                cur.execute(postgreSQL_select_Query)
                #print("Selecting rows from mobile table using cursor.fetchall")
                table_records = cur.fetchall()
                check_value_in_table = False
                for row in table_records:
                    #print(row)
                    if id in row:
                        check_value_in_table = True


            except (Exception, psycopg2.Error) as error:
                print("Error while fetching data from PostgreSQL", error)
            if not check_value_in_table:
                #print(f'{id} added')
                sqlList=f"INSERT INTO properties VALUES {id,properties[0],properties[1]}"
                sqlList = sqlList.replace("None", "NULL")
                cur.execute(sqlList)


        is_active = Check_key_in_dict('is_active',local_product['sm'])
        last_updates = str(Check_key_in_dict('last_updated',local_product['sm']))

        rivals_updated = Check_key_in_dict('rivals_updated',local_product['sm'])
        sm_product_type = Check_key_in_dict('type',local_product['sm'])

        try:
            postgreSQL_select_Query = f"select * from sm_product"

            cur.execute(postgreSQL_select_Query)
            #print("Selecting rows from mobile table using cursor.fetchall")
            table_records = cur.fetchall()
            check_value_in_table = False
            for row in table_records:
                #print(row)
                if id in row:
                    check_value_in_table = True


        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
        if not check_value_in_table:
            #print(f'{id} added')
            sqlList=f"INSERT INTO sm_product VALUES {id,is_active,last_updates,rivals_updated,sm_product_type}"
            sqlList = sqlList.replace("None", "NULL")
            cur.execute(sqlList)


        for item in local_product['stock']:
            stock_date = item['date']
            stock_level = item['stock_level']
            try:
                postgreSQL_select_Query = f"select * from stock"

                cur.execute(postgreSQL_select_Query)
                #print("Selecting rows from mobile table using cursor.fetchall")
                table_records = cur.fetchall()
                check_value_in_table = False
                for row in table_records:
                    #print(row)
                    if id in row:
                        check_value_in_table = True


            except (Exception, psycopg2.Error) as error:
                print("Error while fetching data from PostgreSQL", error)
            if not check_value_in_table:
                #print(f'{id} added')
                sqlList=f"INSERT INTO stock VALUES {id,stock_date,stock_level}"
                sqlList = sqlList.replace("None", "NULL")
                cur.execute(sqlList)

            #con.commit()

    # except IndexError:
    #     break
    #
    # except ValueError:
    #     pass
    # except KeyError:
    #     pass
    # except psycopg2.Error:
    #     pass
    # finally:
        if i % 250 == 0:
            print(i)
        i +=1
        con.commit()


cur.close()
con.close()