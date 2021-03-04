from pymongo import MongoClient
import psycopg2

client = MongoClient()
database = client.huwebshop

db_products = database.products.find()
con = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="kip12345",
)
i = 0
cur = con.cursor()

while True:
    try:
        local_product = db_products[i]
        id = int(local_product['_id'])
        brand = local_product['brand']

        name = local_product['name']
        category = local_product['category']
        gender = local_product['gender']
        discription = local_product['discription']
        sub_category = local_product['sub_category']
        sub_sub_category = local_product['sub_sub_category']
        color = local_product['color']
        fast_mover = local_product['fast_mover']
        herhaalaankoop = local_product['herhaalaankoop']
        product_size = local_product['product_size']
        product_typename = local_product['product_typename']

        selling_price = local_product['price']['selling_price']
        cost_price = local_product['price']['cost_price']
        deeplink = local_product['price']['deeplink']
        price_discription = local_product['price']['description']
        images = local_product['price']['description']
        label = local_product['price']['label']
        mrsp = local_product['price']['mrsp']
        price_properties = local_product['price']['properties']

        is_active = local_product['sm']
        last_updates = local_product['sm']
        rivals_updated = local_product['sm']
        sm_product_type = local_product['sm']



        properties=[]
        for items in local_product['properties']:
            items.split(':')
            properties.append(items)






        cur.execute(f"INSERT INTO product VALUES {id,name,brand,discription,gender, category,sub_category,sub_sub_category, color,fast_mover,herhaalaankoop,product_size,product_typename};")
        con.commit()
        cur.execute(f"INSERT INTO price VALUES {id, cost_price, deeplink, price_discription, selling_price, images, label, mrsp, name, price_properties};")
        con.commit()
        for i in range(0,len(properties)):
            cur.execute(f"INSERT INTO properties VALUES {id,properties[0],properties[1]}")
        con.commit()
        cur.execute(f"INSERT INTO sm_product VALUES {id,is_active,last_updates,rivals_updated,sm_product_type}")

    except IndexError:
        break
    except ValueError:
        pass
    except KeyError:
        pass
    except psycopg2.Error:
        pass
    finally:
        print(id,"succes")

        con.commit()
        i +=1


cur.close()
con.close()