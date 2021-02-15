#testconnection between Python and MongoDB
from pymongo import MongoClient

client = MongoClient()
database = client.huwebshop
products = database.products.find()
# print(products[0]["price"]["selling_price"])

#name and price of first product in collection "products" in database huwebshop:
print(products[0]["name"], products[0]["price"]["selling_price"])


#prints out the name of the first product with a name starting with "R":
try:
    i = 0
    while True:
        product = (products[i]["name"])

        if product[0] == "R" or product[0] == "r":
            print(f'The first product starting with "R": {product}.')
            break

        i += 1
except IndexError:
    print('Something went wrong!')

print((products[0]["price"]["selling_price"]))


#prints out the mean price of all products in the database:
try:
    try:
        j = 0
        price_total = 0
        while True:
            price = products[j]["price"]["selling_price"]

            if type(price) == float: # <= if the price is not in cents but euro's it converts it to cents.
                price = price * 100

            print(price)
            price_total = price_total + price

            j += 1

    except IndexError:
        print('Something went wrong with the index!') # <= index out of range
except KeyError:
    print('Something went wrong with the price!') # <= product no price

print(f'The total price of all products in the database is: {price_total}')

print(f'The mean price of all products in the database is: {price_total / j}.') #~528 cent