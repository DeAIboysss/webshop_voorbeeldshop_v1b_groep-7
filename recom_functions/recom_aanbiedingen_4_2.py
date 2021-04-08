def get_promo_products(tup:tuple,con,cur):
    dict_aanbieding = {}
    for item in tup:
        #print(item)
        cur.execute(f"select pd.sub_sub_category, pt.value from product as pd inner join properties as pt on pd.id = pt.productid where (pd.id = '{item[0]}' and pt.key = 'discount' )")
        record = cur.fetchall()
        cat = record[0][0]
        promo = record[0][1]

        if cat != None and promo != None:
            for _ in range(0,item[1]):
                if f'{cat}_{promo}' in dict_aanbieding :
                    dict_aanbieding[f'{cat}_{promo}'].append(item[0])
                else:
                    dict_aanbieding[f'{cat}_{promo}'] = []
                    dict_aanbieding[f'{cat}_{promo}'].append(item[0])
    for key,value in dict_aanbieding.items():
        key = key.split('_')
        print(key, value)
        if len(value) != int(key[1][0]) and cat != None and promo != None:
            print('incompleet', key)
            sql = f"select lst_product_id from collaborative_recommendations_combination4_2 where (recom_basis = '{key[0]}_{key[1]}')"
            cur.execute(sql)
            products = cur.fetchall()
            print(item,cat,promo,products)
            if products != []:
                return list(products[0][0].split(','))
    return None



#print(get_promo_products(tuples,con,cur))

#time0 = datetime.datetime.now()

def select_combinations(con,cur):
    """
    Selects all distinct categories from the sub sub category column in table product.

        :return: A list with all categories from sub_sub_category.
    """
    sql = """SELECT pd.sub_sub_category, pp.value as promo FROM product pd
            INNER JOIN properties pp
            ON pd.id = pp.productid
            WHERE pp.key = 'discount'
            GROUP BY promo, sub_sub_category;"""
    combinations = []

    cur.execute(sql)
    records = cur.fetchall()

    for record in records:
        combinations.append(f'{record[0]}_{record[1]}')

    print(combinations)
    return combinations

#select_combinations()

#======================================= CREATE TABLES:
def create_new_table(con,cur):
    """
    Creates new tables for every different kind of recommendation if table does not already exist.
        :param table: A string that represents the name of the table.
        :return: None.
    """
    cur.execute("""CREATE TABLE IF NOT EXISTS collaborative_recommendations_combination4_2
                            (recom_basis VARCHAR, lst_product_id VARCHAR);""")
    con.commit()

#create_new_table()

#======================================= SELECT AND INSERT DATA:
def insert_into_tables(base_name, lst_recoms,con,cur):
    """
    Inserts data from insert_different_tables and inserts it in the right columns etc.
        :param base_name: name of the base on which a recommendation is made as a string.
        :param lst_recoms: list with product id's as a string.
    """
    if "'" in base_name:
        replace = base_name.replace("'","''")
        cur.execute("INSERT INTO collaborative_recommendations_combination4_2 VALUES ('%s', '%s');" % (replace, lst_recoms))
    else:
        cur.execute("INSERT INTO collaborative_recommendations_combination4_2 VALUES ('%s', '%s');" % (base_name, lst_recoms))


def select_data_for_inserts(con,cur):
    """
    Asks for the right data and inserts into table.
    """
    for i in select_combinations():
        parted = i.partition('_')
        if parted[0] != None:
            sql = """SELECT productid as id, value as promo,sub_sub_category 
                         FROM product pd 
                         INNER JOIN properties pp 
                         ON pd.id = pp.productid 
                         WHERE pp.key like 'discount' 
                         AND sub_sub_category like '%s'
                         AND value like '%s' 
                         ORDER BY id ASC LIMIT 4;""" % (parted[0].replace("'","''"), parted[2])

        cur.execute(sql)
        records = cur.fetchall()
        recoms = []

        if len(records) == 4:
            for record in records:
                recoms.append(record[0])
                joined = ','.join(recoms)
            insert_into_tables(str(i), joined)

