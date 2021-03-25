import datetime
import psycopg2

time0 = datetime.datetime.now()
content = ['category', 'sub_category', 'sub_sub_category', 'properties']


def database_connection():
    """
    Tries to connect to the relational database and prints the connection result.
    """
    global con
    global cur
    try:
        con = psycopg2.connect(
            host="localhost",
            database="huwebshop",
            user="postgres",
            password="admin")
        cur = con.cursor()
        print('Database connection succes')
    except:
        print('Something went wrong with the database connection')

database_connection()


def list_column_names(name):
    """
    Asks for the name of a list and returns said list.

        :param name: The name of a table.
        :return: A list with all the columns for said table.
    """

    if name == 'sub_sub_category':
        return ['Pijnstillers', 'Multivitaminen', 'Shampoo', 'Kat', 'Toiletpapier_en_vochtige_doekjes', 'Elektronica_accessoires', 'Condooms', 'Batterijen', 'Kunstgebitverzorging', 'Wasverzachter', 'Tandenstokers_floss_en_ragers', 'Meubels', 'Overige_dierverzorging', 'Haaraccessoires', 'Lenzenvloeistof', 'Feestartikelen', 'Wattenschijfjes_en_wattenstaafjes', 'Reisziekte', 'Textielverf', 'Pleisters', 'Accessoires', 'Zwangerschap', 'Gewrichten', 'Oogschaduw', 'Reiniging_vaatwasser', 'Nagellakremovers', 'Schoenen_slippers_en_sloffen', 'Voetschimmel', 'Foundation_en_concealer', 'Blush', 'Media', 'Scheerschuim_en_scheergel', 'Kinderkleding', 'Geschenksets', 'Zwangerschapsvitamines', 'Homeopathisch', 'Overige_huishoudelijke_artikelen', 'Mondverfrissers', 'Bad_en_douche', 'Kaarsen', 'Huishoudelijke_apparaten', 'Voetdeodorant', 'Aftershave', 'Babyhaartjes_bad_en_douche', 'Afwasmiddel', 'Kaarten', 'Poeder', 'Carnaval', 'Keukenpapier', 'Nagellak', 'Mondwater_en_spray', 'Sieraden_en_bijoux', 'Make_up_remover_en_reiniging', 'Bandages_en_windsels', 'Dames_nachtmode', 'Vlekkenverwijderaars', 'Onzuivere_huid_en_acne', 'Zwemluiers', 'Koffie', 'Deodorant', 'Tampons', 'Overige_voedingssuplementen', 'Haarkuur_en_haarmasker', 'Kappersproducten', 'Schoonmaken', 'Muziek', 'Knutselen_en_hobby', 'Glijmiddelen_en_seksspeeltjes', 'Kerst', 'Kantoor_benodigdheden', 'Dames_brillen', 'Oor_en_mond', 'Chips', 'Anti_lekbekers', 'Speelgoed', 'Herengeuren', 'Bordspellen', 'Highlighters_en_bronzers', 'Toiletblokken', 'Luchtwegen_en_verkoudheid', 'Weerstand', 'Enkelvoudige_vitaminen', 'Damesgeuren', 'Sportverzorging', 'Lipliner', 'Dames_kleding', 'Dvd_en_Blue_ray', 'Luierbroekjes_en_pyjamabroekjes', 'Tissues_en_zakdoekjes', 'Lipverzorging', 'Botten', 'Overige_elektronika', 'Watten', 'Heren_nachtmode', 'Scheermesjes', 'Make_up_accessoires', 'Lenzen', 'Maaltijdvervangers', 'Blaas', 'Baby_accessoires', 'Sportdranken', 'Sportvoeding', 'EHBO', 'Oogcreme_en_serum', 'Cartridges', 'Mini_tandpasta', 'Ontspanning_en_rust', 'Babydoekjes', 'Kunstnagels', 'Foto_en_film', 'Gezichtsmasker_man', 'Spierwrijfmiddelen', 'Man', 'Boeken', 'Baby_speelgoed', 'Flesvoeding', 'Lampen', 'Insectenbestrijding', 'Babykleding', 'Mineralen', 'Haarserum', 'Keuken_artikelen', 'Baby_en_kinderaccessoires', 'Luizen', 'Tandpasta', 'Heren_brillen', 'Verzorgende_voetcremes', 'Dames_ondergoed', 'Mascara', 'Kinderbestek', 'Flessen_en_flessenspenen', 'Reiniging', 'Eelt_en_harde_huid', 'Supplementen', 'Dames_accessoires', 'Ontharingscreme_wax_en_hars', 'Pasen', 'Vaatwastabletten', 'Outdoor_en_vrije_tijd', 'Natuurlijke_gezondheid', 'Beeld_en_geluid', 'Fopspenen', 'Handcremes', 'Tablets_en_computers', 'Huidverzorging_en_koortslip', 'Koffers', 'Nachtcreme', 'Vakantie', 'Leesbrillen', 'Maandverband', 'Mini_scheerschuim_en_scheergel', 'Inlegkruisjes', 'Intiemverzorging', 'Vaginale_schimmel', 'Wratten', 'Tuinartikelen', 'Mini_bad_en_douche', 'Tassen', 'Mama_verzorging', 'Voetverzorging', 'Hond', 'Verlichting', 'Vibrators_en_dildos', 'Uiterlijk', 'Creme', 'Wenkbrauwproducten', 'Haarstyling', 'Wasmiddel', 'Oordoppen', 'Handzeep_en_handgel', 'Lipgloss', 'Kalknagels', 'Energie', 'Snacks_en_snoep', 'Stoppen_met_roken', 'Incontinentie', 'Mini_olie_en_lotion', 'Heren_ondergoed', 'Wondontsmetting', 'Kind', 'Luiers', 'Gezichtsmasker', 'Thee', 'Zonnebrand_en_aftersun', 'Lipstick', 'Energy_drank', 'Zwangerschapstest_en_ovulatietest', 'Telefonie', 'Woonaccessoires', 'Heren_accessoires', 'Aambeien', 'Scheren', 'Dagcreme', 'Mini_shampoo_en_conditioner', 'Haarkleuring', 'Overige_dranken', 'Wondverzorging', 'Allergieen', 'Bodylotion_en_bodymilk', 'Hart_en_visolie', 'Toilettassen', 'Elektrische_tandenborstels', 'Toiletreinigers', 'Halloween', 'Huishoudelijk_textiel', 'Tandenborstels', 'Panties_en_sokken', 'Luchtverfrissers', 'Valentijn', 'Sportartikelen', 'Conditioner', 'Mini_deodorant_en_geuren', 'Persoonlijke_verzorging', 'Sokken', 'Baby_huidverzorging', 'Scheerapparaten', 'Patty_Brard_Collectie', 'Spijsvertering', 'Mini_haarstyling', 'Reiniging_man']
    elif name == 'personality_type':
        return ['LEAVER_Unisex', 'LEAVER_None', 'LEAVER_Kinderen', 'LEAVER_Senior', 'LEAVER_B2B', 'LEAVER_Gezin', 'LEAVER_8719497835768', 'LEAVER_Baby', 'LEAVER_Man', 'LEAVER_Grootverpakking', 'LEAVER_Vrouw', 'BOUNCER_Unisex', 'BOUNCER_None', 'BOUNCER_Kinderen', 'BOUNCER_Senior', 'BOUNCER_B2B', 'BOUNCER_Gezin', 'BOUNCER_8719497835768', 'BOUNCER_Baby', 'BOUNCER_Man', 'BOUNCER_Grootverpakking', 'BOUNCER_Vrouw', 'FUN_SHOPPER_Unisex', 'FUN_SHOPPER_None', 'FUN_SHOPPER_Kinderen', 'FUN_SHOPPER_Senior', 'FUN_SHOPPER_B2B', 'FUN_SHOPPER_Gezin', 'FUN_SHOPPER_8719497835768', 'FUN_SHOPPER_Baby', 'FUN_SHOPPER_Man', 'FUN_SHOPPER_Grootverpakking', 'FUN_SHOPPER_Vrouw', 'JUDGER_Unisex', 'JUDGER_None', 'JUDGER_Kinderen', 'JUDGER_Senior', 'JUDGER_B2B', 'JUDGER_Gezin', 'JUDGER_8719497835768', 'JUDGER_Baby', 'JUDGER_Man', 'JUDGER_Grootverpakking', 'JUDGER_Vrouw', 'BROWSER_Unisex', 'BROWSER_None', 'BROWSER_Kinderen', 'BROWSER_Senior', 'BROWSER_B2B', 'BROWSER_Gezin', 'BROWSER_8719497835768', 'BROWSER_Baby', 'BROWSER_Man', 'BROWSER_Grootverpakking', 'BROWSER_Vrouw', 'COMPARATOR_Unisex', 'COMPARATOR_None', 'COMPARATOR_Kinderen', 'COMPARATOR_Senior', 'COMPARATOR_B2B', 'COMPARATOR_Gezin', 'COMPARATOR_8719497835768', 'COMPARATOR_Baby', 'COMPARATOR_Man', 'COMPARATOR_Grootverpakking', 'COMPARATOR_Vrouw', 'SHOPPING_CART_Unisex', 'SHOPPING_CART_None', 'SHOPPING_CART_Kinderen', 'SHOPPING_CART_Senior', 'SHOPPING_CART_B2B', 'SHOPPING_CART_Gezin', 'SHOPPING_CART_8719497835768', 'SHOPPING_CART_Baby', 'SHOPPING_CART_Man', 'SHOPPING_CART_Grootverpakking', 'SHOPPING_CART_Vrouw', 'BUYER_Unisex', 'BUYER_None', 'BUYER_Kinderen', 'BUYER_Senior', 'BUYER_B2B', 'BUYER_Gezin', 'BUYER_8719497835768', 'BUYER_Baby', 'BUYER_Man', 'BUYER_Grootverpakking', 'BUYER_Vrouw', 'COMPARER_Unisex', 'COMPARER_None', 'COMPARER_Kinderen', 'COMPARER_Senior', 'COMPARER_B2B', 'COMPARER_Gezin', 'COMPARER_8719497835768', 'COMPARER_Baby', 'COMPARER_Man', 'COMPARER_Grootverpakking', 'COMPARER_Vrouw']
    else:
        return ['Pijnstillers', 'Multivitaminen', 'Shampoo', 'Kat', 'Toiletpapier en vochtige doekjes', 'Elektronica accessoires', 'Condooms', 'Batterijen', 'Kunstgebitverzorging', 'Wasverzachter', 'Tandenstokers, floss & ragers', 'Meubels', 'Overige dierverzorging', 'Haaraccessoires', 'Lenzenvloeistof', 'Feestartikelen', 'Wattenschijfjes en wattenstaafjes', 'Reisziekte', 'Textielverf', 'Pleisters', 'Accessoires', 'Zwangerschap', None, 'Gewrichten', 'Oogschaduw', 'Reiniging vaatwasser', 'Nagellakremovers', 'Schoenen, slippers en sloffen', 'Voetschimmel', 'Foundation & concealer', 'Blush', 'Media', 'Scheerschuim en scheergel', 'Kinderkleding', 'Geschenksets', 'Zwangerschapsvitamines', 'Homeopathisch', 'Overige huishoudelijke artikelen', 'Mondverfrissers', 'Bad en douche', 'Kaarsen', 'Huishoudelijke apparaten', 'Voetdeodorant', 'Aftershave', 'Babyhaartjes, bad en douche', 'Afwasmiddel', 'Kaarten', 'Poeder', 'Carnaval', 'Keukenpapier', 'Nagellak', 'Mondwater & spray', 'Sieraden & bijoux', 'Make-up remover & reiniging', 'Bandages en windsels', 'Dames nachtmode', 'Vlekkenverwijderaars', 'Onzuivere huid & acne', 'Zwemluiers', 'Koffie', 'Deodorant', 'Tampons', 'Overige voedingssuplementen', 'Haarkuur en haarmasker', 'Kappersproducten', 'Schoonmaken', 'Muziek', 'Knutselen en hobby', 'Glijmiddelen en seksspeeltjes', 'Kerst', 'Kantoor benodigdheden', 'Dames brillen', 'Oor en mond', 'Chips', 'Anti-lekbekers', 'Speelgoed', 'Herengeuren', 'Bordspellen', 'Highlighters en bronzers', 'Toiletblokken', 'Luchtwegen en verkoudheid', 'Weerstand', 'Enkelvoudige vitaminen', 'Damesgeuren', 'Sportverzorging', 'Lipliner', 'Dames kleding', 'Dvd en blue-ray', 'Luierbroekjes en pyjamabroekjes', 'Tissues en zakdoekjes', 'Lipverzorging', 'Botten', 'Overige elektronika', 'Watten', 'Heren nachtmode', 'Scheermesjes', 'Make-up accessoires', 'Lenzen', 'Maaltijdvervangers', 'Blaas', 'Baby accessoires', 'Sportdranken', 'Sportvoeding', 'EHBO', 'Oogcreme en serum', 'Cartridges', 'Mini tandpasta', 'Ontspanning en rust', 'Babydoekjes', 'Kunstnagels', 'Foto en film', 'Gezichtsmasker man', 'Spierwrijfmiddelen', 'Man', 'Boeken', 'Baby speelgoed', 'Flesvoeding', 'Lampen', 'Insectenbestrijding', 'Babykleding', 'Mineralen', 'Haarserum', 'Keuken artikelen', 'Baby- en kinderaccessoires', 'Luizen', 'Tandpasta', 'Heren brillen', 'Verzorgende voetcremes', 'Dames ondergoed', 'Mascara', 'Kinderbestek', 'Flessen en flessenspenen', 'Reiniging', 'Eelt en harde huid', 'Supplementen', 'Dames accessoires', 'Ontharingscreme, wax en hars', 'Pasen', 'Vaatwastabletten', 'Outdoor en vrije tijd', 'Natuurlijke gezondheid', 'Beeld en geluid', 'Fopspenen', 'Handcremes', 'Tablets en computers', 'Huidverzorging en koortslip', 'Koffers', 'Nachtcreme', 'Vakantie', 'Leesbrillen', 'Maandverband', 'Mini scheerschuim en scheergel', 'Inlegkruisjes', 'Intiemverzorging', 'Vaginale schimmel', 'Wratten', 'Tuinartikelen', 'Mini bad en douche', 'Tassen', 'Mama verzorging', 'Voetverzorging', 'Hond', 'Verlichting', "Vibrators en dildo''s", 'Uiterlijk', 'Creme', 'Wenkbrauwproducten', 'Haarstyling', 'Wasmiddel', 'Oordoppen', 'Handzeep en handgel', 'Lipgloss', 'Kalknagels', 'Energie', 'Snacks en snoep', 'Stoppen met roken', 'Incontinentie', 'Mini olie en lotion', 'Heren ondergoed', 'Wondontsmetting', 'Kind', 'Luiers', 'Gezichtsmasker', 'Thee', 'Zonnebrand en aftersun', 'Lipstick', 'Energy drank', 'Zwangerschapstest en ovulatietest', 'Telefonie', 'Woonaccessoires', 'Heren accessoires', 'Aambeien', 'Scheren', 'Dagcreme', 'Mini shampoo en conditioner', 'Haarkleuring', 'Overige dranken', 'Wondverzorging', 'Allergieen', 'Bodylotion en bodymilk', 'Hart en visolie', 'Toilettassen', 'Elektrische tandenborstels', 'Toiletreinigers', 'Halloween', 'Huishoudelijk textiel', 'Tandenborstels', 'Panties en sokken', 'Luchtverfrissers', 'Valentijn', 'Sportartikelen', 'Conditioner', 'Mini deodorant en geuren', 'Persoonlijke verzorging', 'Sokken', 'Baby huidverzorging', 'Scheerapparaten', 'Patty Brard Collectie', 'Spijsvertering', 'Mini haarstyling', 'Reiniging man']


#======================================= CREATE TABLES:

def create_new_table(recom_basis):
    """
    Creates new tables for every different kind of recommendation if table does not already exist.

        :param table: A string that represents the name of the table.
        :return: None.
    """

    '''DELETE ALL TABLES:'''

    cur.execute("DROP TABLE IF EXISTS collaborative_recommendations;")


    cur.execute("""CREATE TABLE IF NOT EXISTS collaborative_recommendations
                            (recom_basis VARCHAR,lst_product_id VARCHAR);""")
    con.commit()

for i in list_column_names('sub_sub_category'):
     create_new_table(i)

for j in list_column_names('personality_type'):
     create_new_table(j)



#======================================= SELECT AND INSERT DATA:

def select_data(sql):
    """
    Reads a query and returns the rows of the selected data.

        :param sql: A list with queries as strings.
        :return: A list with records as tuples.
    """
    cur.execute(sql)
    records = cur.fetchall()

    return records


def insert_into_tables(records, table_name):
    """
    Takes data from function select_data and inserts it into the correct table.

        :param records: A list (records) with rows as tuples.
        :param table_name: Table name in the form of a string.
        :return: None.
    """
    print(table_name)
    print(records)

    # for row in records:
    #     cur.execute("INSERT INTO %s VALUES ('%s', '%s', '%s', '%s', '%s', '%s');"%(table_name, row[0], row[1], row[2], row[3], row[4], row[5]))


def sub_sub_category_inserts():
    """
    Content filtering based on sub_sub_category and if the product has a promo.
    Runs a function insert_into_tables with the right data for the different recommendation sub_sub_category tables.
    """
    names_sub_sub_category = sorted(list_column_names('names_sub_sub_category'), key=lambda empty: (empty is None, empty))
    sub_sub_category = sorted(list_column_names('sub_sub_category'), key=lambda empty: (empty is None, empty))

    for i, value in enumerate(sub_sub_category):
        if names_sub_sub_category[i] == None:
            query = "SELECT productid as id, value as promo, name as product_name,sub_sub_category, gender as target_audience, selling_price as price FROM product pd INNER JOIN properties pp ON pd.id = pp.productid WHERE pp.key like 'discount' AND sub_sub_category like '%s' ORDER BY id ASC LIMIT 4;" % (names_sub_sub_category[i])
        else:
            query = "SELECT productid as id, value as promo, name as product_name,sub_sub_category, gender as target_audience, selling_price as price FROM product pd INNER JOIN properties pp ON pd.id = pp.productid WHERE pp.key like 'discount' AND sub_sub_category like '%s' ORDER BY id ASC LIMIT 4;" % (names_sub_sub_category[i].replace("'", "''"))

        insert_into_tables(select_data(query), f"rec_{sub_sub_category[i]}".lower())


#sub_sub_category_inserts()


def personality_type_inserts():
    """
    Content filtering based on gender of a product and segment of a profile and if the product has a promo.
    Runs a function insert_into_tables with the right data for the different recommendation sub_sub_category tables.
    """
    new_personality_type = sorted(list_column_names('personality_type'))

    for i, value in enumerate(new_personality_type):
        value = value.lower()

        if value.startswith('shopping_cart') or value.startswith('fun_shopper'):
            segment = "_".join(value.split("_", 2)[:2])
            gender = "_".join(value.split("_", 2)[2:])

            query = "SELECT pp.productid as id, value as promo, name as product_name, sub_sub_category, gender as target_audience, selling_price as price FROM product pd INNER JOIN properties pp ON pd.id = pp.productid INNER JOIN viewed_before vb ON pd.id = vb.productid INNER JOIN profile pf ON pf.profile_id = vb.profileprofile_id WHERE pp.key like 'discount' AND (pd.gender like '%s' OR pd.gender like INITCAP('%s')) AND (pf.segment like '%s'OR pf.segment like UPPER('%s')) LIMIT 4;" % (gender, gender, segment, segment)

        else:
            value = value.split("_", 1)
            segment = value[0]
            gender = value[1]

            query = "SELECT pp.productid as id, value as promo, name as product_name, sub_sub_category, gender as target_audience, selling_price as price FROM product pd INNER JOIN properties pp ON pd.id = pp.productid INNER JOIN viewed_before vb ON pd.id = vb.productid INNER JOIN profile pf ON pf.profile_id = vb.profileprofile_id WHERE pp.key like 'discount' AND (pd.gender like '%s' OR pd.gender like INITCAP('%s')) AND (pf.segment like '%s'OR pf.segment like UPPER('%s')) LIMIT 4" % (gender, gender, segment, segment)

        insert_into_tables(select_data(query), f"type_{new_personality_type[i]}".lower())


#personality_type_inserts()


con.commit()
cur.close()
con.close()

print(datetime.datetime.now() - time0)   # <= prints how long the program took to run.