from pymongo import MongoClient
import psycopg2
from random import randint
import datetime
import connect


def close(con,cur):
    '''closes connection with database
    :param cur cursor
    :param con connection
    '''
    cur.close()
    con.close()


def wipecontentfilter(con,cur):
    cur.execute('DROP TABLE IF EXISTS contentfilter; CREATE TABLE contentfilter(sub_sub_category varchar(255),gender varchar(255),brand varchar(255),id varchar(255),name varchar(255))')
    con.commit()


def wipecollaborationfilter(con,cur):
    cur.execute('DROP TABLE IF EXISTS collaborative_recommendations_behaviour; CREATE TABLE collaborative_recommendations_behaviour(product_id varchar(255),segment varchar(255))')
    con.commit()


def contentfilter(nieuweproducten:bool,con,cur):
    '''
    Deze functie maakt een tabel aan met daarin vier producten per subsubcategory per gender.
    Deze producten kunnen worden gereccomend als de klant op producten heeft geklikt en er dus bekent is wel gender en subsubcategory er worden bekeken.
    nieuweproducten is een variabele die true is als er nieuwe producten zijn
    '''

    if nieuweproducten:
        cur.execute('select sub_sub_category,gender from product')
        data = cur.fetchall()

        subsubcategorylist = []
        genderlist = []

        for i in data:
            if i[1] not in subsubcategorylist:
                subsubcategorylist.append(i[1])
            if i[2] not in genderlist:
                genderlist.append(i[2])
        print(subsubcategorylist)
        print(genderlist)

    subsubcategorylist = ['Nagellak',None, 'Nagellakremovers', 'Kunstnagels', 'Make-up accessoires', 'Oogschaduw', 'Foundation & concealer', 'Mascara', 'Lipstick', 'Wenkbrauwproducten', 'Reiniging', 'Poeder', 'Blush', 'Tandpasta', 'Shampoo', 'Elektrische tandenborstels', 'Haarkuur en haarmasker', 'Conditioner', 'Deodorant', 'Scheermesjes', 'Mondwater & spray', 'Aftershave', 'Bad en douche', 'Handzeep en handgel', 'Lipverzorging', 'Scheren', 'Scheerschuim en scheergel', 'Haarstyling', 'Toiletblokken', 'Handcremes', 'Homeopathisch', 'Lampen', 'Herengeuren', 'Incontinentie', 'Haarserum', 'Haarkleuring', 'Nachtcreme', 'Wasmiddel', 'Bodylotion en bodymilk', 'Schoonmaken', 'Gezichtsmasker', 'Baby huidverzorging', 'Wondverzorging', 'Pleisters', 'Damesgeuren', 'Toiletreinigers', 'Vaatwastabletten', 'Reiniging vaatwasser', 'Luchtwegen en verkoudheid', 'Pijnstillers', 'Mini deodorant en geuren', 'Wasverzachter', 'Babyhaartjes, bad en douche', 'Kerst', 'Dagcreme', 'Snacks en snoep', 'Mini bad en douche', 'Panties en sokken', 'Huishoudelijk textiel', 'Kunstgebitverzorging', 'Tandenborstels', 'Textielverf', 'Tampons', 'Afwasmiddel', 'Outdoor en vrije tijd', 'Luiers', 'Babydoekjes', 'Geschenksets', 'Glijmiddelen en seksspeeltjes', 'Vakantie', 'Mini tandpasta', 'Mini olie en lotion', 'Zonnebrand en aftersun', 'Mondverfrissers', 'Luchtverfrissers', 'Batterijen', 'Inlegkruisjes', 'Mini haarstyling', 'Make-up remover & reiniging', 'Maandverband', 'Mini shampoo en conditioner', 'Insectenbestrijding', 'Overige huishoudelijke artikelen', 'Vlekkenverwijderaars', 'Oogcreme en serum', 'Dames brillen', 'Mini scheerschuim en scheergel', 'Creme', 'Condooms', 'Intiemverzorging', 'Overige dierverzorging', 'Reiniging man', 'Huidverzorging en koortslip', 'Dames kleding', 'Spijsvertering', 'Oor en mond', 'Multivitaminen', 'Kind', 'Energie', 'Kaarsen', 'Tandenstokers, floss & ragers', "Vibrators en dildo's", 'Voetverzorging', 'Onzuivere huid & acne', 'Keuken artikelen', 'Ontharingscreme, wax en hars', 'Media', 'Woonaccessoires', 'Flessen en flessenspenen', 'Kappersproducten', 'Overige dranken', 'Speelgoed', 'Baby- en kinderaccessoires', 'Sportdranken', 'Toilettassen', 'Lenzen', 'Lenzenvloeistof', 'Sokken', 'Toiletpapier en vochtige doekjes', 'Stoppen met roken', 'Kalknagels', 'Heren ondergoed', 'Weerstand', 'Hond', 'Wattenschijfjes en wattenstaafjes', 'Kat', 'Babykleding', 'Tuinartikelen', 'Oordoppen', 'Halloween', 'Feestartikelen', 'Kantoor benodigdheden', 'Baby accessoires', 'Tissues en zakdoekjes', 'Verzorgende voetcremes', 'Beeld en geluid', 'Anti-lekbekers', 'Fopspenen', 'Spierwrijfmiddelen', 'Voetdeodorant', 'Voetschimmel', 'Sportverzorging', 'Luizen', 'Baby speelgoed', 'Boeken', 'Sportartikelen', 'Zwangerschapstest en ovulatietest', 'Gezichtsmasker man', 'Highlighters en bronzers', 'Mama verzorging', 'Dames ondergoed', 'Carnaval', 'Supplementen', 'Tablets en computers', 'Haaraccessoires', 'Keukenpapier', 'Botten', 'Enkelvoudige vitaminen', 'Overige voedingssuplementen', 'Uiterlijk', 'Ontspanning en rust', 'Tassen', 'Wondontsmetting', 'Lipliner', 'Blaas', 'Hart en visolie', 'Mineralen', 'Gewrichten', 'Elektronica accessoires', 'Flesvoeding', 'Chips', 'Sieraden & bijoux', 'Koffie', 'Zwemluiers', 'Sportvoeding', 'Verlichting', 'Zwangerschapsvitamines', 'Knutselen en hobby', 'Watten', 'Wratten', 'Lipgloss', 'Patty Brard Collectie', 'Dames accessoires', 'Luierbroekjes en pyjamabroekjes', 'Thee', 'Bandages en windsels', 'Kinderbestek', 'Persoonlijke verzorging', 'EHBO', 'Foto en film', 'Heren accessoires', 'Man', 'Kinderkleding', 'Zwangerschap', 'Koffers', 'Cartridges', 'Eelt en harde huid', 'Huishoudelijke apparaten', 'Overige elektronika', 'Muziek', 'Scheerapparaten', 'Dvd en blue-ray', 'Schoenen, slippers en sloffen', 'Accessoires', 'Kaarten', 'Dames nachtmode', 'Leesbrillen', 'Heren brillen', 'Vaginale schimmel', 'Natuurlijke gezondheid', 'Pasen', 'Meubels', 'Telefonie', 'Valentijn', 'Energy drank', 'Maaltijdvervangers', 'Allergieen', 'Bordspellen', 'Heren nachtmode', 'Reisziekte', 'Aambeien']
    genderlist = ['Unisex',None, 'Vrouw', 'Man', 'Gezin', 'B2B', 'Kinderen', 'Baby', 'Senior', 'Grootverpakking', '8719497835768']

    wipecontentfilter(con,cur)

    for category in subsubcategorylist:
        for gender in genderlist:
            cur.execute('SELECT sub_sub_category,gender,brand,id,name FROM product WHERE sub_sub_category = %s and gender =%s LIMIT 4',(category,gender))
            data = cur.fetchall()
            cur.executemany('INSERT INTO contentfilter VALUES(%s,%s,%s,%s,%s)',data)

    con.commit()



def collaborativefilter(nieuwesegments:bool,con,cur):
    '''
    Deze functie maakt een tabel aan met daarin de vier meest gereccomende producten per segment.
    Deze producten kunnen worden gereccomend als de klant een segment heeft toegewezen gekregen.
    :param nieuwesegments is een variabele die true is als er segments zijn
    :param cur cursor
    :param con connection
    '''
    if nieuwesegments:
        cur.execute('SELECT DISTINCT segment FROM profile')
        segs = cur.fetchall()
        segments =[]
        for segment in segs:
            if list(segment)[0] is not None and list(segment)[0].lower() not in segments:
                segments.append(list(segment)[0].lower())

    segments = ['leaver', 'bouncer', 'fun_shopper', 'judger', 'browser', 'comparator', 'shopping_cart', 'buyer', 'comparer']

    wipecollaborationfilter(con,cur)

    segmentdict = {}

    cur.execute('''SELECT previously_recommended.productid as product_id,profile.segment FROM profile 
                INNER JOIN previously_recommended ON profileprofile_id = profile.profile_id
                INNER JOIN similars ON similars.profileprofile_id = profile.profile_id
                INNER JOIN viewed_before ON viewed_before.profileprofile_id = profile.profile_id 
                WHERE profile.segment is not null ''')
    products = cur.fetchall()


    for product,seg in products:
        segment = seg.lower()
        if segment in segmentdict.keys():
            if product in segmentdict[segment]:
                segmentdict[segment][product] +=1
            else:
                segmentdict[segment][product] = 1
        else:
            segmentdict[segment] = {product:1}



    for segment in segments:
        highestfreq0 = ['',0]
        highestfreq1 = ['',0]
        highestfreq2 = ['',0]
        highestfreq3 = ['',0]

        id_frequency_dict = segmentdict[segment]
        for id,frequency in id_frequency_dict.items():
            if frequency > highestfreq0[1]:
                highestfreq3 = highestfreq2
                highestfreq2 = highestfreq1
                highestfreq1 = highestfreq0
                highestfreq0 = [id,frequency]
            elif frequency > highestfreq1[1]:
                highestfreq3 = highestfreq2
                highestfreq2 = highestfreq1
                highestfreq1 = [id,frequency]
            elif frequency > highestfreq2[1]:
                highestfreq3 = highestfreq2
                highestfreq2 = [id,frequency]
            elif frequency > highestfreq3[1]:
                highestfreq3 = [id,frequency]
        data =[]
        data.append((highestfreq0[0],segment))
        data.append((highestfreq1[0],segment))
        data.append((highestfreq2[0],segment))
        data.append((highestfreq3[0],segment))

        cur.executemany('INSERT INTO collaborative_recommendations_behaviour VALUES(%s,%s)',data)
        con.commit()



def main():
    '''driver code'''
    time0 = datetime.datetime.now()
    con,cur =connect.connection()
    #contentfilter(True)
    collaborativefilter(False,con,cur)
    close(con,cur)
    print(datetime.datetime.now()-time0)


if __name__ == '__main__':
    main()

