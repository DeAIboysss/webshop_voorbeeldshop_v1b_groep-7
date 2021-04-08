def getpricerange(con,cur):
    '''
    Determines what the priceclasses are per 10 percent of the products.
    :param con: connection with pgadmin used to commit
    :param cur: cursor in pgadmin used to execute sql
    :return: returns the ranges in tuples
    '''
    cur.execute('SELECT selling_price FROM product')
    products = cur.fetchall()
    prices = []
    percent = 10
    for product in products:
        #print(type(list(product)[0]))
        if list(product)[0] != None:
            if list(product)[0] != 0:
                prices.append(list(product)[0])
    lengte =0
    for i in prices:
        if i == 0:
            lengte+=1
    print(lengte)
    prices.sort()
    l = len(prices)

    rangelist = []
    for i in range(100//percent+1):
        if i != 0:
            rangelist.append(prices[(l//percent)*i-1])
        if i != 100//percent:
            rangelist.append(prices[(l//percent)*i])
    pricerange = []
    for index in range(1,20,2):
        pricerange.append((rangelist[index-1],rangelist[index]))
    return pricerange

def wipetablepricerange(con,cur):
    '''
    Creates empty table to insert filter data into.
    :param con: connection with pgadmin used to commit
    :param cur: cursor in pgadmin used to execute sql
    '''
    cur.execute('DROP TABLE IF EXISTS collaborative_recommendations_pricerange; CREATE TABLE collaborative_recommendations_pricerange(price_cat varchar(255),id varchar(255))')
    con.commit()

def getcatandpricedata(pricerange,con,cur):
    '''
    Gets data that will later be inserted into pgadmin filter table
    :param pricerange: classes used to categorize products
    :param con: connection with pgadmin used to commit
    :param cur: cursor in pgadmin used to execute sql
    :return: returns an array with tuples containing sub_sub_category combined with priceclass and products
    '''
    cur.execute('SELECT sub_sub_category, selling_price, id FROM product')
    products = cur.fetchall()
    sscatdict = {}
    for sscat,price,id in products:
        whichrange = 0
        for prices in pricerange:
            if type(price) != type(None):
                if price < prices[1]:
                    pricerangeproduct =whichrange
                    break
                if whichrange ==9:
                    pricerangeproduct = 9
                whichrange +=1
        sp =str(sscat)+'_'+str(pricerangeproduct)
        if sp in sscatdict:
            if len(sscatdict[sp]) <4:
                sscatdict[sp].append(id)
        else:
            sscatdict[sp] = [id]

    removekeys = []
    for key in sscatdict.keys():
        if len(sscatdict[key]) !=4:
            removekeys.append(key)


    for key in removekeys:
        sscatdict.pop(key)
    instertproof =[]
    for key, value in sscatdict.items():
        instertproof.append((key,str(value[0])+','+str(value[1])+','+str(value[2])+','+str(value[3])))

    return instertproof
def insertpriceclass(datapriceclass,con,cur):
    """
    Inserts data into price class filter
    :param datapriceclass: Array of tuples containing products and sub_sub_category combined with priceclass
    :param con: connection with pgadmin used to commit
    :param cur: cursor in pgadmin used to execute sql
    """
    cur.executemany('INSERT INTO collaborative_recommendations_pricerange VALUES(%s,%s);',datapriceclass)
    con.commit()

