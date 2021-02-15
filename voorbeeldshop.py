from pymongo import MongoClient

client = MongoClient()
database = client.huwebshop
products = database.products.find()
print(products[0])