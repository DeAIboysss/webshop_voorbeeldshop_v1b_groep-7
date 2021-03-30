import connect
import datetime
def getpricerange(percent,con,cur):
    cur.execute('SELECT selling_price FROM product')
    products = cur.fetchall()
    prices = []
    for product in products:
        if list(product)[0] != None:
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
    return rangelist

def main():

    con,cur = connect.connection()
    time0=datetime.datetime.now()
    var = getpricerange(10,con,cur)
    for i in range(0,len(var),2):
        print(var[i],var[i+1])
    print(datetime.datetime.now()-time0)
    cur.close()
    con.close()

if __name__ == '__main__':
    main()