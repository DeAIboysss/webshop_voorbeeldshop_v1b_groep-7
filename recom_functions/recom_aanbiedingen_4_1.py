from .connect import connection
con, cur = connection("huwebshop", "admin")
#======================================= CREATE TABLE:
def create_new_table():
    """
    Creates a new table with products
        :param table: A string that represents the name of the recom base.
    """
    cur.execute("""CREATE TABLE IF NOT EXISTS collaborative_recommendations_combination
                            (recom_basis VARCHAR, lst_product_id VARCHAR);""")
    con.commit()

#create_new_table("aanbieding")

#======================================= SELECT AND INSERT DATA:
def insert_into_tables(base_name, lst_recoms):
    """
    Inserts data from insert_different_tables and inserts it in the right columns etc.
        :param base_name: name of the base on which a recommendation is made as a string.
        :param lst_recoms: list with product id's as a string.
    """
    cur.execute("INSERT INTO collaborative_recommendations_combination VALUES ('%s', '%s');" % (base_name, lst_recoms))


def insert_different_tables():
    """
    Asks for the right data and calls on insert function to put data in the right columns.
    """
    sql = """SELECT productid as id, value as promo
    FROM product pd 
    INNER JOIN properties pp 
    ON pd.id = pp.productid 
    WHERE pp.key like 'discount' 
    ORDER BY id ASC LIMIT 4;"""

    cur.execute(sql)
    records = cur.fetchall()
    recoms = []

    for record in records:
        recoms.append(record[0])
        joined = ','.join(recoms)

    print(recoms)
    print(joined)

    insert_into_tables("aanbieding", joined)

#insert_different_tables()


def read_aanbiedingen(con,cur):
    """
    Reads all data from table "collaborative_recommendations_combination" and returns these as a list.

        :param con: makes a connection to the database.
        :param cur: makes it possible to call upon SQL methods.
        :return: a list with 4 product id's.
    """
    con = con
    cur = cur
    cur.execute("SELECT * FROM collaborative_recommendations_combination;")
    records = cur.fetchall()
    cur.close()
    con.close()
    ids = str(records[0][1])
    split = ids.split(',')
    return split