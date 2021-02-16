from pymongo import MongoClient


client = MongoClient()
database = client.huwebshop
products = database.products.find()

i=0
totalprice =0
count = 0
rproduct =[]

while True:
    try:
        product = products[i]
        if product['_id'] == '1':
            id1product =product

        if product['name'][0] == 'R' and type(rproduct) == type([]):
           rproduct = product['name']

        if type(product['price']['selling_price']) == type(1.1):
            totalprice += product['price']['selling_price'] * 100
        elif type(product['price']['selling_price']) == type(1):
            totalprice += product['price']['selling_price']

        count+=1
    except IndexError:
        break
    except ValueError:
        pass
    except KeyError:
        pass
    finally:
        i +=1

with open('2a_results.txt','a') as f:
    f.write('name = '+id1product['name']+' price = '+str(id1product['price']['selling_price'])+' --> Product where id = 1 \n')
    f.write(rproduct+' --> Name of first product where name starts with "R"\n')
    f.write('€ '+str(round(totalprice/(count*100),2))+' --> Average price\n')

