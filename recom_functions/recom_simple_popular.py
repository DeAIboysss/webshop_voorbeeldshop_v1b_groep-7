from connect import connection
con, cur = connection(con, cur)

def create_new_table(con, cur):
    """
    Creates new tables for every different kind of recommendation if table does not already exist.

        :param con: makes a connection to the database.
        :param cur: makes it possible to call upon SQL methods.
    """

    cur.execute("""CREATE TABLE IF NOT EXISTS collaborative_recommendations_popular_test
                            (recom_basis VARCHAR,lst_product_id VARCHAR);""")
    con.commit()

create_new_table(con, cur)


def insert_into_tables(base_name, lst_recoms):
    """
    Inserts data from insert_different_tables and inserts it in the right columns etc.

        :param base_name: name of the base on which a recommendation is made as a string.
        :param lst_recoms: list with product id's as a string.
    """
    cur.execute("INSERT INTO collaborative_recommendations_popular_test VALUES ('%s', '%s');" % (base_name, lst_recoms))


def insert_different_tables():
    """
    Asks for the right data and calls on insert function to put data in the right columns.
    """
    sql = """SELECT product_id, count(product_id) as aantal FROM orders o
                INNER JOIN product pd
                ON pd.id = o.product_id
                WHERE pd.selling_price > 0
                GROUP BY product_id
                ORDER BY aantal DESC LIMIT 4;"""

    cur.execute(sql)
    records = cur.fetchall()
    recoms = []

    for record in records:
        recoms.append(record[0])
    joined = ','.join(recoms)

    insert_into_tables('meest_verkocht', joined)


def read_meest_verkocht(con,cur):
    """
    Selects the most ordered products from the database.

        :param con: makes a connection to the database.
        :param cur: makes it possible to call upon SQL methods.
    """
    cur.execute("SELECT * FROM collaborative_recommendations_popular_test WHERE recom_basis = 'meest_verkocht'")
    records = cur.fetchall()
    ids = str(records[0][1])
    split = ids.split(',')
    return split

insert_different_tables()
con.commit()
