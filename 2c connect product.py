from pymongo import MongoClient
import psycopg2


client = MongoClient()
database = client.huwebshop
products = database.products.find()

print(products[0]['_id'])
print(products[0]['brand'])
print(products[0]['name'])
print(products[0]['price']['selling_price'])
print(products[0]['category'])
print(products[0]['gender'])
i=0
dictionary_products = {}


while True and i<101:
    try:

        product = products[i]
        id = product['_id']
        brand = product['brand']
        name = product['name']
        price = product['price']['selling_price']
        category = product['category']
        gender = product['gender']
        dictionary_products[id] = [brand,name,price,category,gender]

    except IndexError:
        break
    except ValueError:
        pass
    except KeyError:
        pass
    finally:
        i +=1


con = psycopg2.connect(
    host="localhost",
    database="product2c",
    user="postgres",
    password="Vicecity_007",
)
cur = con.cursor()
for id,list_values in dictionary_products.items():
    #print(id,list_values)
    if type(id) == type('str'):
        try:

            id = int(id)
            print(id,type(id))


        except:
            print('niet gelukt')

    cur.execute(f"INSERT INTO product VALUES {id,list_values[0],list_values[1],list_values[2],list_values[3],list_values[4]};")

con.commit()
cur.close()
con.close()