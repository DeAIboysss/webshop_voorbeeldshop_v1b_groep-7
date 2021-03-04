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
    # product table
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

        cur.execute(f"INSERT INTO product VALUES {id,name,brand,discription,gender,category,sub_category,sub_sub_category, color,fast_mover,herhaalaankoop,product_size,product_typename};")
        con.commit()
    except IndexError:
        break
    except ValueError:
        pass
    except KeyError:
        pass
    except psycopg2.Error:
        pass


    # price table
    try:
        selling_price = local_product['price']['selling_price']
        cost_price = local_product['price']['cost_price']
        deeplink = local_product['price']['deeplink']
        price_discription = local_product['price']['description']
        images = local_product['price']['description']
        label = local_product['price']['label']
        mrsp = local_product['price']['mrsp']
        price_properties = local_product['price']['properties']

        cur.execute(f"INSERT INTO price VALUES {id, cost_price, deeplink, price_discription, selling_price, images, label, mrsp, name, price_properties};")
        con.commit()
    except IndexError:
        break
    except ValueError:
        pass
    except KeyError:
        pass
    except psycopg2.Error:
        pass


    # properties table
    try:
        properties = []
        for items in local_product['properties']:
            items.split(':')
            properties.append(items)
        for x in range(0,len(properties)):
            cur.execute(f"INSERT INTO properties VALUES {id,properties[0],properties[1]}")
        con.commit()
    except IndexError:
        break
    except ValueError:
        pass
    except KeyError:
        pass
    except psycopg2.Error:
        pass


    # SM table
    try:
        is_active = local_product['sm']
        last_updates = local_product['sm']
        rivals_updated = local_product['sm']
        sm_product_type = local_product['sm']

        cur.execute(f"INSERT INTO sm_product VALUES {id,is_active,last_updates,rivals_updated,sm_product_type}")
        con.commit()
    except IndexError:
        break
    except ValueError:
        pass
    except KeyError:
        pass
    except psycopg2.Error:
        pass


    # stock table
    try:
        stock_date = local_product['stock']
        stock_level=local_product['stock_level']
        for i in range(0,len(local_product['stock'])):
            stock_date = local_product['stock'][i]
            stock_level = local_product['stock_level'][i]
            cur.execute(f"INSERT INTO stock VALUES {id,stock_date,stock_level}")
            con.commit()

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
        i +=1


cur.close()
con.close()