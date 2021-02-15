#testconnection between Python and MongoDB
from pymongo import MongoClient

client = MongoClient()
database = client.huwebshop
products = database.products.find()
# print(products[0]["price"]["selling_price"])

#name and price of first product in collection "products" in database huwebshop:
print(products[0]["name"], products[0]["price"]["selling_price"])

pr = 0
try:
    for i in products:
        product = (products[0]["name"])
        if product[0] == "R":
            print(product)
except:
    print('Something went wrong')