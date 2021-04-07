import datetime

time0 = datetime.datetime.now()

t0 = datetime.datetime.now()
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
    This function scans the given profile for all the viewed products
    and gets the most viewed combination of sub_sub_category and properties.doelgroep.
    the return wil provide the most chosen properties.doelgroep and the most chosen sub_category of this profile.
    :param profile_id: The profile we want to retrieve data from.
    :return: the most chosen combination.
    """
    lst_base_1 = []
    lst_base_2 = []

    cur.execute(f"select sm.productid from similars sm where sm.profileprofile_id = '{profile_id}' Union all select sm.productid from viewed_before sm where sm.profileprofile_id = '{profile_id}'")
    records = cur.fetchall()

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
    These products are bases on the Record_1 and Record_2 most vieuwed combinations
    For example, i shop for garden stuff and for underwear, i buy garden stuf once and i buy multiple sorts of underwear
    The function wil search for other profiles with most viewed item in the category underwear and the gender man
    :param profile_id: the profile i want to have a recommendation for
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
                highest.append(high_withprod[max(combinations, key=combinations.get)])
                del combinations[max(combinations, key=combinations.get)]
        recommend_products = []
        for products in highest:
            for prod in products:
                recommend_products.append(prod)
        if len(highest) != 0:
            if len(highest[0])>=4:
                string_recommend_products = ",".join(recommend_products[:4])
            else:
                return None
            if len(recommend_products)>= 4:
                cur.execute(f"insert into collaborative_recommendations values('{record_1}_{record_2}','{string_recommend_products}') ")
                con.commit()
                return recommend_products
            else:
                return None
        else:
            return None
