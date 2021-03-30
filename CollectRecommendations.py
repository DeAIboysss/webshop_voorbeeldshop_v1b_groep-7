from pymongo import MongoClient
import psycopg2
from random import randint
import datetime
import connect



def close(con,cur):
    '''closes connection with database'''

    cur.close()
    con.close()

def collect_contentfilter(profileid,cur):
    '''

    :param profileid: profile id
    :param cur: cursor used to iterate over items in database
    :param con: connection to database
    :return: product ids
    '''
    product_ids2 = []
    cur.execute("SELECT segment FROM profile WHERE profile_id = '%s'"%(profileid))
    segment = cur.fetchall()
    segment = list(segment)[0][0]
    if type(segment) == type(None) or segment == 'bouncer' or segment == 'leaver':
        segment = 'buyer'
    else:
        segment = segment.lower()

    cur.execute("SELECT product_id FROM collaborative_recommendations_behaviour WHERE segment = '%s'"%(segment))
    product_ids = cur.fetchall()
    for i in list(product_ids):
        product_ids2.append(i[0])

    return product_ids2

def main():
    '''driver code'''
    time0 = datetime.datetime.now()
    con,cur =connect.connection()
    print(collect_contentfilter('59dce306a56ac6edb4c12838',cur))
    print(collect_contentfilter('59dce303a56ac6edb4c10fcf',cur))

    close(con,cur)
    print(datetime.datetime.now()-time0)


if __name__ == '__main__':
    main()
