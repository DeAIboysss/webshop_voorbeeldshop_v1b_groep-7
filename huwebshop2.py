from pymongo import MongoClient
import psycopg2




client = MongoClient()
database = client.huwebshop


db_profiles = database.profiles.find()

con = psycopg2.connect(
    host="localhost",
    database="huwebshop2",
    user="postgres",
    password="Vicecity_007",
)
cur = con.cursor()

def recommend():



cur.close()
con.close()
