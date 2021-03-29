from pymongo import MongoClient
import psycopg2
from random import randint
import datetime



def wipecollaborationfilter(cur,con):
    """

    :param cur:
    :param con:
    :return:
    """
    cur.execute('DROP TABLE IF EXISTS collaborationfilter; CREATE TABLE collaborationfilter(product_id varchar(255),segment varchar(255))')
    con.commit()



def collaborativefilter(nieuwesegments:bool,con,cur):
    '''
    Deze functie maakt een tabel aan met daarin de vier meest gereccomende producten per segment.
    Deze producten kunnen worden gereccomend als de klant een segment heeft toegewezen gekregen.
    nieuwesegments is een variabele die true is als er segments zijn
    '''
    if nieuwesegments:
        cur.execute('SELECT DISTINCT segment FROM profile')
        segs = cur.fetchall()
        segments =[]
        for segment in segs:
            if list(segment)[0] is not None and list(segment)[0].lower() not in segments:
                segments.append(list(segment)[0].lower())

    segments = ['leaver', 'bouncer', 'fun_shopper', 'judger', 'browser', 'comparator', 'shopping_cart', 'buyer', 'comparer']

    wipecollaborationfilter(cur,con)

    segmentdict = {}

    cur.execute('''SELECT previously_recommended.productid as product_id,profile.segment FROM profile 
                INNER JOIN previously_recommended ON profileprofile_id = profile.profile_id
                INNER JOIN similars ON similars.profileprofile_id = profile.profile_id
                INNER JOIN viewed_before ON viewed_before.profileprofile_id = profile.profile_id 
                WHERE profile.segment is not null ''')
    products = cur.fetchall()


    for product,seg in products:
        segment = seg.lower()
        if segment in segmentdict.keys():
            if product in segmentdict[segment]:
                segmentdict[segment][product] +=1
            else:
                segmentdict[segment][product] = 1
        else:
            segmentdict[segment] = {product:1}



    for segment in segments:
        highestfreq0 = ['',0]
        highestfreq1 = ['',0]
        highestfreq2 = ['',0]
        highestfreq3 = ['',0]

        id_frequency_dict = segmentdict[segment]
        for id,frequency in id_frequency_dict.items():
            if frequency > highestfreq0[1]:
                highestfreq3 = highestfreq2
                highestfreq2 = highestfreq1
                highestfreq1 = highestfreq0
                highestfreq0 = [id,frequency]
            elif frequency > highestfreq1[1]:
                highestfreq3 = highestfreq2
                highestfreq2 = highestfreq1
                highestfreq1 = [id,frequency]
            elif frequency > highestfreq2[1]:
                highestfreq3 = highestfreq2
                highestfreq2 = [id,frequency]
            elif frequency > highestfreq3[1]:
                highestfreq3 = [id,frequency]
        data =[]
        data.append((highestfreq0[0],segment))
        data.append((highestfreq1[0],segment))
        data.append((highestfreq2[0],segment))
        data.append((highestfreq3[0],segment))

        cur.executemany('INSERT INTO collaborationfilter VALUES(%s,%s)',data)
        con.commit()

from recom_functions.connect import connection


def main():
    '''driver code'''
    time0 = datetime.datetime.now()
    con,cur = connection('opdracht2_final', 'kip12345')
    #contentfilter(False)
    collaborativefilter(True,con,cur)
    print(datetime.datetime.now()-time0)
    cur.close()
    con.close()




if __name__ == '__main__':
    main()

