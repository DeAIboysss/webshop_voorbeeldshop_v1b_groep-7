from .create_recom_price_range import getpricerange

def collect_pricerangefilter(productid,con,cur):
    '''
    :param profileid: Current user, given by site.
    :param cur: cursor in pgadmin used to execute sql
    :param con: connection to database
    :return: returns product ids collected from price range filter
    '''
    cur.execute("SELECT sub_sub_category, selling_price FROM product WHERE id = '%s'"%(productid))

    sscat,price = cur.fetchall()[0]
    pricerange = getpricerange(con,cur)
    whichrange = 0
    for prices in pricerange:
        if type(price) != type(None):
            if price < prices[1]:
                pricerangeproduct =whichrange
                break
            if whichrange ==9:
                pricerangeproduct = 9
            whichrange +=1

    sscat_pricerange = str(sscat) + '_' + str(pricerangeproduct)
    print(sscat_pricerange)
    cur.execute("SELECT id FROM collaborative_recommendations_pricerange WHERE price_cat = '%s'"% sscat_pricerange)
    product_ids = cur.fetchall()

    if product_ids != []:
        product_ids = product_ids[0][0].split(',')
    else:
        product_ids = None
    return product_ids
