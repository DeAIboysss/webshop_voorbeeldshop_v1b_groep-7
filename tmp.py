from pymongo import MongoClient
import psycopg2
import datetime


def GetProfiledata():

    global time0
    i = 0
    biglist =[]

    # time1 = datetime.datetime.now()
    # lasttime = datetime.datetime.now() -datetime.datetime.now()

    #while True  and i <itemindex:
    for profile in database.profiles.find({},{"_id":1,"order":1,"recommendations":1}):
        try:

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


            biglist.append((profile_id,latest_activity,latest,count,segment))

            # if i % 10000 == 0 :
            #     print(i)
            #     if i != 0 and i != 1000:
            #         print((time0 - time1) -lasttime)
            #         lasttime =time0 - time1
            #
            #     time1 = time0
            #     time0 = datetime.datetime.now()

            i +=1
        except IndexError:
            return biglist

    print(datetime.datetime.now()-time0)
    return biglist



client = MongoClient()
database = client.huwebshop


# iets doen met db_profiles


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

profiles = GetProfiledata()
#print(profiles)

# for p in profiles:
#
#     cur.execute((f"INSERT INTO profile VALUES {p[0],p[1],p[2],p[3],p[4]};").replace("None", "NULL"))




cur.executemany("INSERT INTO profile VALUES (%s,%s,%s,%s,%s);",profiles)

con.commit()
cur.close()
con.close()
print(datetime.datetime.now()-time0)
