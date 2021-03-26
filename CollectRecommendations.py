from pymongo import MongoClient
import psycopg2
from random import randint
import datetime

def connect():
    '''opens connection with database'''
    global client
    global database
    global db_profiles
    global con
    global cur

    client = MongoClient()
    database = client.huwebshop

    db_profiles = database.profiles.find()

    con = psycopg2.connect(
        host="localhost",
        database="huwebshop",
        user="postgres",
        password="Vicecity_007",
    )
    cur = con.cursor()


def close():
    '''closes connection with database'''
    global cur
    global con
    cur.close()
    con.close()

def collect_contentfilter(profileid):

    product_ids2 = []
    cur.execute("SELECT segment FROM profile WHERE profile_id = '%s'"%(profileid))
    segment = cur.fetchall()
    segment = list(segment)[0][0]
    if type(segment) == type(None):
        segment = 'leaver'
    else:
        segment = segment.lower()

    cur.execute("SELECT product_id FROM collaborationfilter WHERE segment = '%s'"%(segment))
    product_ids = cur.fetchall()
    for i in list(product_ids):
        product_ids2.append(i[0])

    return product_ids2

def main():
    '''driver code'''
    time0 = datetime.datetime.now()
    connect()
    collect_contentfilter('59dce306a56ac6edb4c12838')
    collect_contentfilter('59dce303a56ac6edb4c10fcf')

    close()
    print(datetime.datetime.now()-time0)


if __name__ == '__main__':
    main()
