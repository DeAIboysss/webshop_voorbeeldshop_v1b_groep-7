from pymongo import MongoClient
import psycopg2


def WriteToPostgreSQL(itemindex,increment):

    i = itemindex


    while True  and i <(itemindex+increment):
        try:

            local_profile = db_profiles[i]


            #profiles table
            profile_id = str(local_profile["_id"])

            if 'meta' in local_profile:
                has_utm_hash = local_profile["meta"]["has_utm_hash"]
                has_device = local_profile["meta"]["has_device"]
                has_email = local_profile["meta"]["has_email"]
                random = local_profile["meta"]["random"]
            else:
                has_utm_hash = None
                has_device = None
                has_email = None
                random = None

            if 'sm' in local_profile:
                created = str(local_profile["sm"]["created"])
                created_by = local_profile["sm"]["created_by"]
            else:
                created = None
                created_by = None

            if 'order' in local_profile:
                if 'latest' in local_profile["order"]:
                    latest = str(local_profile["order"]["latest"])
                else:
                    latest = None
                if 'count' in local_profile["order"]:
                    count = local_profile["order"]["count"]
                else:
                    count = None
                if 'first' in local_profile["order"]:
                    first = str(local_profile["order"]["first"])
                else:
                    first = None
            else:
                latest = None
                count = None
                first = None

            if 'recommendations' in local_profile:
                latest_activity = str(local_profile["recommendations"]["timestamp"])
                timestamp = str(local_profile["recommendations"]["timestamp"])
                segment = local_profile["recommendations"]["segment"]
                latest_visit = str(local_profile["recommendations"]["latest_visit"])
                total_viewed_count = local_profile["recommendations"]["total_pageview_count"]
                total_pageview_count = local_profile["recommendations"]["total_viewed_count"]
            else:
                latest_activity = None
                timestamp = None
                segment = None
                latest_visit = None
                total_viewed_count = None
                total_pageview_count = None


            cur.execute((f"INSERT INTO profile VALUES {profile_id,latest_activity,has_utm_hash,has_device,has_email,random,created,created_by,latest,count,first,timestamp,segment,latest_visit,total_viewed_count,total_pageview_count};").replace("None", "NULL"))



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
            i +=1




client = MongoClient()
database = client.huwebshop

#db_products = database.products.find()
db_profiles = database.profiles.find()

con = psycopg2.connect(
    host="localhost",
    database="huwebshop",
    user="postgres",
    password="Vicecity_007",
)
cur = con.cursor()
for i in range(220059,2082649,100):

    WriteToPostgreSQL(i,100)

cur.close()
con.close()
# id = int(local_product['_id'])
# brand = local_product['brand']
#
# name = local_product['name']
# category = local_product['category']
# gender = local_product['gender']
# discription = local_product['discription']
# sub_category = local_product['sub_category']
# sub_sub_category = local_product['sub_sub_category']
# color = local_product['color']
# fast_mover = local_product['fast_mover']
# herhaalaankoop = local_product['herhaalaankoop']
# product_size = local_product['product_size']
# product_typename = local_product['product_typename']
#
# selling_price = local_product['price']['selling_price']
# cost_price = local_product['price']['cost_price']
# deeplink = local_product['price']['deeplink']
# price_discription = local_product['price']['description']
# images = local_product['price']['description']
# label = local_product['price']['label']
# mrsp = local_product['price']['mrsp']
# price_properties = local_product['price']['properties']
#
# is_active = local_product['sm']
# last_updates = local_product['sm']
# rivals_updated = local_product['sm']
# sm_product_type = local_product['sm']



# properties=[]
# for items in local_product['properties']:
#     items.split(':')
#     properties.append(items)






# cur.execute(f"INSERT INTO product VALUES {id,name,brand,discription,gender, category,sub_category,sub_sub_category, color,fast_mover,herhaalaankoop,product_size,product_typename};")
# con.commit()
# cur.execute(f"INSERT INTO price VALUES {id, cost_price, deeplink, price_discription, selling_price, images, label, mrsp, name, price_properties};")
# con.commit()
# for i in range(0,len(properties)):
#     cur.execute(f"INSERT INTO properties VALUES {id,properties[0],properties[1]}")
# con.commit()
# cur.execute(f"INSERT INTO sm_product VALUES {id,is_active,last_updates,rivals_updated,sm_product_type}")
# con.commit()
