import psycopg2
from pymongo import MongoClient


def get_connection():
    client = MongoClient()
    database = client.huwebshop
    products = database.products.find()
    print(products[0]["name"], products[0]["price"]["selling_price"])



try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.close()
    connection.commit()
except:
    print("Connection error with the database.")
