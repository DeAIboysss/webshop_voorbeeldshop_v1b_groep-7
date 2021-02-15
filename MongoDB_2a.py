from pymongo import MongoClient

client = MongoClient()
database = client.huwebshop
products = database.products.find()
i=0
while True:
    try:
        product = products[i]
        if product['_id'] == '1':
            print(product)
            break
    except:
        break
    i +=1

# from pymongo import MongoClient
#
# client = MongoClient()
# database = client.huwebshop
# products = database.products.find()
# i=0
# while True:
#
#     try:
#         product = products[i]
#         print(product)
#     except:
#         break
#     i +=1