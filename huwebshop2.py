from pymongo import MongoClient
import psycopg2


def WriteToPostgreSQL(itemindex):

    i = itemindex
    start = i

    while True  and i >0:
        try:
            #print(profiles)
            if (start - i)%1000 == 0:
                profiles = GetProfiles(start-i)

            local_profile = profiles[0]


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


            cur.execute((f"INSERT INTO profile VALUES {profile_id,latest_activity,latest,count,segment};").replace("None", "NULL"))



            #cur.execute(f"INSERT INTO profile VALUES ('a',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);")





            #print(local_profile["sm"]["created"])






        except IndexError:
            break
        # except ValueError:
        #     print('Value error')
        except KeyError as ke:
            print(str(ke))
            #pass


        except psycopg2.Error as pe:
            print(pe)
            #print(profile_id)
        finally:
            #print(id,"succes")

            con.commit()
            i -=1


def GetProfiles(itemindex):
    return db_profiles[itemindex:]

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
# for i in range(98241,,100):
WriteToPostgreSQL(2082649)

cur.close()
con.close()
