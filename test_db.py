from pymongo import MongoClient

client = MongoClient()
database = client.huwebshop
products = database.products.find()
#print(products[0]["name"],products[0]["price"]["selling_price"])

# Wat is de naam en prijs van het eerste product in de database?
print(products[0]["name"],products[0]["price"]["selling_price"])
# Geef de naam van het eerste product waarvan de naam begint met een 'R'?
try:
    i = 0
    while True:
        pr = products[i]["name"]
        if pr[0] == "R":
            print(pr)
            break;
        i+=1
except IndexError:
    print("list completed")

# Wat is de gemiddelde prijs van de producten in de database?
try:
    i = 0
    while True:
        pr = products[i]["name"]
        if pr[0] == "R":
            print(pr)
            break;
        i+=1
except IndexError:
    print("list completed")