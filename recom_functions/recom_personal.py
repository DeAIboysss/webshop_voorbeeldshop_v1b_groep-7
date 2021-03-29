import datetime
import psycopg2

time0 = datetime.datetime.now()

# con = psycopg2.connect(
#     host="localhost",
#     database="opdracht2_final",
#     user="postgres",
#     password="kip12345",
# )
# cur = con.cursor()

t0 = datetime.datetime.now()
def create_content_recommendation_table(colmn, value, order):
    """
    This function creates a table with 4 recommended items that ar the outcome of the inputted parameters.
    :param colmn: The colm witch the recommendation is based on, so for example sub_category
    :param value: The value this colmn had to have, for brand this can be nivea and for sub_sub_category this can be deoderant
    :param order: The order the products are filtered i, this an be on ID or on selling_price or in every toher colmn name
    :return: A created table in pgadmin
    """

    sql = []
    cur.execute("""CREATE TABLE IF NOT EXISTS recommendation_%s 
                    (id VARCHAR PRIMARY KEY,
                     name VARCHAR,
                     brand VARCHAR,
                     type VARCHAR,
                     category VARCHAR,
                     subcategory VARCHAR,
                     subsubcategory VARCHAR,
                     targetaudience VARCHAR,
                     selling_price INTEGER,
                     deal VARCHAR,
                     description VARCHAR,
                     stock INTEGER );""" % (value))
    con.commit()
    cur.execute("DELETE FROM recommendation_%s"% (value))
    cur.execute(f"SELECT * FROM product  WHERE ({colmn} = '{value}' and selling_price > 0 and stock_level > 0)  ORDER BY {order} ASC limit 4 ")  # % (table,colmn,value,))
    records = cur.fetchall()
    for record in records:
        cur.execute(f"SELECT * FROM properties WHERE (productid = '{record[0]}') ORDER BY productid ASC")
        properties = cur.fetchall()
        deal = None
        types =  None
        doelgroep =None
        for prop in properties:
            if prop[1] == 'discount':
                deal = prop[2]
            if prop[1] =='soort':
                types = prop[2]
            if prop[1] == 'doelgroep':
                doelgroep = prop[2]
        sql.append((record[0], record[1], record[3], types, record[8], record[9], record[10], doelgroep, record[2],deal, record[6],record[13]))
    print(f"recommendation_{value} table created/filled")
    cur.executemany(f"INSERT INTO recommendation_{value} VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",sql)
    con.commit()


#create_content_recommendation_table('sub_sub_category', 'Deodorant', 'selling_price')
#create_content_recommendation_table('brand','Nivea','selling_price')

def get_highest_key(array:list):
    '''
    Returns meest voorkomende naam in array
    :param array: de ingegeven list
    :return: Meest gekozen
    '''
    dict_count ={}
    for array in array:
        if array not in dict_count:
            dict_count[array] = 1
        elif array in dict_count:
            dict_count[array] += 1
    return max(dict_count, key=dict_count.get)

def get_most_used_bases(profile_id:str,con,cur):
    """
    This funciton scans the given profile for all the viewed products and gets the inputted colmn values from these products.
    These values are called base_1 and base_2,
    for example if i chose gender and sub_category,
    the return wil provide the most chosen gender and the most chosen sub_category of this profile.
    :param profile_id: The profile we want to retrive data from
    :param base_1: The first colmn name
    :param base_2: The second colmn name
    :return: the most chosen base_1 and the most chosen base_2
    """
    lst_base_1 = []
    lst_base_2 = []

    cur.execute(f"select sm.productid from similars sm where sm.profileprofile_id = '{profile_id}' Union all select sm.productid from viewed_before sm where sm.profileprofile_id = '{profile_id}'")
    records = cur.fetchall()
    #print(records)
    combi = []
    ownviewd = []
    for record in records:
        ownviewd.append(record[0])
        cur.execute(f"select sub_sub_category from product where id ='{record[0]}'")
        cat = cur.fetchall()
        if len(cat)>0:
            lst_base_1.append(cat[0][0])
        cur.execute(f"select value from properties where productid ='{record[0]}' and key = 'doelgroep'")
        dg = cur.fetchall()
        if len(dg) > 0:
            lst_base_2.append(dg[0][0])


    #print(records)
    # for prod in records:
    #     ownviewd.append(prod[2])
    #     if len(prod) != 0:
    #         lst_base_1.append(prod[1])
    #         lst_base_2.append(prod[0])

    if len(lst_base_1) != 0:
        high_base_1 = get_highest_key(lst_base_1)
    else:
        high_base_1 = None
    if len(lst_base_2) != 0:
        high_base_2 = get_highest_key(lst_base_2)
    else:
        high_base_2 = None
    return high_base_1,high_base_2,ownviewd

def get_simmilar_profiles(profile_id:str,con,cur):
    """
    This function wil get 4 new recommended products for the givven profile.
    the fucntion checks first if this recommendation combination already had bin done and wil copy the results if it is
    These products are bases on the base_1 and base_2 most vieuwed combinations
    For example, i shop for garden stuff and for underwear, i buy garden stuf once and i buy multiple sorts of underwear
    The function wil search for other profiles with most viewed item in the category underwear and the gender man
    :param profile_id: the profile i want to have a recommendation for
    :param base_1: the first parameter to search for
    :param base_2: the second parameter
    :return: 4 products that other users viewed with the base_1 and base_2 paramters
    """
    con = con
    cur = cur
    record_2, record_1, own_viewed = get_most_used_bases(profile_id,con,cur)
    if record_1 == None or record_2 == None:
        return None
    record_2 = record_2.replace("'", "''")
    record_1 = record_1.replace("'", "''")

    if record_1!=None and "'" in record_1:
        record_1 = record_1.replace("'","")
    cur.execute("""CREATE TABLE IF NOT EXISTS collaborative_recommendations
                        (recom_basis VARCHAR,lst_product_id VARCHAR);""")
    con.commit()
    cur.execute(f"Select lst_product_id from collaborative_recommendations where(recom_basis ='{record_1}_{record_2}' ) ")
    prev_recoms = cur.fetchall()

    if len(prev_recoms) != 0:
        return prev_recoms[0][0].replace('[','').replace(']','').replace(' ','').split(',')
    else:

        cur.execute(f"select vb.profileprofile_id,vb.productid from viewed_before vb inner join product pd on vb.productid = pd.id inner join properties pt on pt.productid = pd.id where pd.sub_sub_category = '{record_2}' and pt.value = '{record_1}'")
        profID = cur.fetchall()
        combinations = {}
        highest = []
        high_withprod = {}
        if len(profID) != 0:
            for id in profID:
                #print(id)
                if id[0] not in high_withprod:
                    high_withprod[id[0]] = []
                    high_withprod[id[0]].append(id[1])
                else:
                    high_withprod[id[0]].append(id[1])
                if id[0] not in combinations:
                    combinations[id[0]] = 1
                else:
                    combinations[id[0]] +=1
            for x in range(0,3):
                #print(max(combinations, key=combinations.get),combinations[max(combinations, key=combinations.get)])
                highest.append(high_withprod[max(combinations, key=combinations.get)])
                del combinations[max(combinations, key=combinations.get)]
        #print(highest)
        recommend_products = []

        for products in highest:
            for prod in products:
                recommend_products.append(prod)
        #print (recommend_products)
        string_recommend_products =''
        x=0
        if len(highest) != 0:
            if len(highest[0])>=4:
                string_recommend_products = ",".join(recommend_products[:4])
            else:
                return None
            #print(string_recommend_products)
            if len(recommend_products)>= 4:
                cur.execute(f"insert into collaborative_recommendations values('{record_1}_{record_2}','{string_recommend_products}') ")
                con.commit()
                return recommend_products
            else:
                return None
        else:
            return None

