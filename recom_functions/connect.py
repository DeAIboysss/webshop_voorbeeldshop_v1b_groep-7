import psycopg2

def connection(database:str,ww:str):
    con = psycopg2.connect(
        host="localhost",
        database=database,
        user="postgres",
        password=ww,
    )
    cur = con.cursor()
    return con,cur