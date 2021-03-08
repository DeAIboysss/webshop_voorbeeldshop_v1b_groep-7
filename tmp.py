from pymongo import MongoClient
import psycopg2
import datetime


def GetProfiledata():

    global time0
    i = 0
    profiles =[]
    previously_recommended = []
    similars =[]
    viewed_before=[]

    #while True  and i <itemindex:
    for profile in database.profiles.find({},{"_id":1,"order":1,"recommendations":1,"previously_recommended":1,"similars":1,"viewed_before":1}):

        local_profile =profile # db_profiles[i]

        #profiles table
        profile_id = str(local_profile["_id"])


        if 'order' in local_profile:
            if 'latest' in local_profile["order"]:
                latest = str(local_profile["order"]["latest"])
            else:
                latest = None
            if 'count' in local_profile["order"]:
                count = local_profile["order"]["count"]
            else:
                count = None
        else:
            latest = None
            count = None

        if 'recommendations' in local_profile:
            latest_activity = str(local_profile["recommendations"]["timestamp"])
            segment = local_profile["recommendations"]["segment"]
        else:
            latest_activity = None
            segment = None


        profiles.append((profile_id,latest_activity,latest,count,segment))

        if "previously_recommended" in local_profile:
            for product in local_profile["previously_recommended"]:
                previously_recommended.append((product,profile_id))
        if "recommendations" in local_profile:
            if "similars" in local_profile["recommendations"]:
                for product in local_profile["recommendations"]["similars"]:
                    similars.append((product,profile_id))

            if "viewed_before" in local_profile["recommendations"]:
                for product in local_profile["recommendations"]["viewed_before"]:
                    viewed_before.append((product,profile_id))


        i +=1


    print(datetime.datetime.now()-time0)

    return profiles,previously_recommended,similars,viewed_before





##buitenfuntie:

client = MongoClient()
database = client.huwebshop



con = psycopg2.connect(
    host="localhost",
    database="huwebshop",
    user="postgres",
    password="Vicecity_007",
)
cur = con.cursor()

time0 = datetime.datetime.now()
with open("message (12).txt","r") as ddl:
    for line in ddl:
        cur.execute(line)


con.commit()

profiles,previously_recommended,similars,viewed_before = GetProfiledata()


cur.executemany("INSERT INTO profile VALUES (%s,%s,%s,%s,%s);",profiles)
cur.executemany("INSERT INTO previously_recommended VALUES (%s,%s);",previously_recommended)
cur.executemany("INSERT INTO similars VALUES (%s,%s);",similars)
cur.executemany("INSERT INTO viewed_before VALUES (%s,%s);",viewed_before)
con.commit()
cur.close()
con.close()
print(datetime.datetime.now()-time0)
