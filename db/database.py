import psycopg2
import constants

# Connect to your postgres DB
conn = psycopg2.connect(f"dbname={constants.DBNAME} user={constants.USER} password={constants.PASSWORD}")
print("Connection réussie")

def update(table, id, data):
    cur = conn.cursor()
    sql = f"UPDATE {table} SET"

    compt = 0
    for key, value in data.items():
        if compt<len(data)-1:
            sql+=f" {key} = {value},"
        else:
            sql+=f" {key} = {value}"
        compt+=1

    sql += f" WHERE id={id};"
    try:
         cur.execute(sql)

    except Exception as e:
        print(f"Attention ! Erreur : {e}")

    finally:
        cur.close()

update("client", "test", {"a": "1", "b": "2"})

def delete(table, id):
    cur = conn.cursor()
    sql = f"DELETE FROM {table} WHERE id = {id};"
    cur.close()

def select(nom_table):
    try:
        cursor = conn.cursor()
        query = f"SELECT * FROM {nom_table};"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    except Exception as e:
        print(f"Attention ! Erreur : {e}")

    finally:
        cursor.close()

select("customer_family")
    