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

insert_different_tables()


def read_aanbiedingen(con,cur, recom_code):
    """
    Reads all data from table "collaborative_recommendations_combination" and returns these as a list.

        :return: a list with 4 product id's.
    """
    recom_code = 6
    con = con
    cur = cur
    cur.execute("SELECT * FROM collaborative_recommendations_combination;")
    records = cur.fetchall()
    cur.close()
    con.close()
    ids = str(records[0][1])
    split = ids.split(',')
    return split


con.commit()
print(datetime.datetime.now() - time0)  # <= prints how long the program took to run.