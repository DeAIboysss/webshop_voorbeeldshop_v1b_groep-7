import datetime
from connect import connection

con, cur = connection("huwebshop", "admin")
time0 = datetime.datetime.now()

#======================================= CREATE TABLES:
def create_new_table(recom_basis):
    """
    Creates new tables for every different kind of recommendation if table does not already exist.
        :param table: A string that represents the name of the table.
        :return: None.
    """
    cur.execute("""CREATE TABLE IF NOT EXISTS collaborative_recommendations_combination
                            (recom_basis VARCHAR, lst_product_id VARCHAR);""")
    con.commit()

create_new_table("aanbieding")

#======================================= SELECT AND INSERT DATA:
def insert_into_tables(base_name, lst_recoms):
    """
    Inserts data from insert_different_tables and inserts it in the right columns etc.
        :param base_name: name of the base on which a recommendation is made as a string.
        :param lst_recoms: list with product id's as a string.
    """
    if "'" in base_name:
        replace = base_name.replace("'","''")
        cur.execute("INSERT INTO collaborative_recommendations_combination VALUES ('%s', '%s');" % (replace, lst_recoms))
    else:
        cur.execute("INSERT INTO collaborative_recommendations_combination VALUES ('%s', '%s');" % (base_name, lst_recoms))


def select_sub_sub_category():
    """
    Selects all distinct categories from the sub sub category column in table product.

        :return: A list with all categories from sub_sub_category.
    """
    sql = "SELECT DISTINCT sub_sub_category FROM product"
    categories = []

    cur.execute(sql)
    records = cur.fetchall()

    for record in records:
        categories.append(record[0])

    print(categories)
    return categories


def insert_different_tables():
    """
    Asks for the right data and calls on insert function to put data in the right columns.
    """
    for i in select_sub_sub_category():
        if i != None:
            sql = """SELECT productid as id, value as promo,sub_sub_category 
            FROM product pd 
            INNER JOIN properties pp 
            ON pd.id = pp.productid 
            WHERE pp.key like 'discount' 
            AND sub_sub_category like '%s' 
            ORDER BY id ASC LIMIT 4;""" % (i).replace("'", "''")

        cur.execute(sql)
        records = cur.fetchall()
        recoms = []

        for record in records:
            recoms.append(record[0])
            joined = ','.join(recoms)

        print(recoms)
        print(joined)

        insert_into_tables(str(i), joined)

insert_different_tables()


def read_aanbiedingen(con,cur, recom_code): # <= evt extra variabele meegeven die sub_sub_category aangeeft.
    """
    Reads all data from table "collaborative_recommendations_combination" and returns these as a list.

        :return: a list with 4 product id's.
    """
    recom_code = 6
    con = con
    cur = cur
    cur.execute("SELECT * FROM collaborative_recommendations_combination WHERE recom_basis = 'Pijnstillers';") # '%s';") % (sub_sub_category)   # <= variabele sub_sub_category aflezen van items in winkelwagen
    records = cur.fetchall()
    cur.close()
    con.close()
    ids = str(records[0][1])
    split = ids.split(',')
    return split


con.commit()
print(datetime.datetime.now() - time0)   # <= prints how long the program took to run.