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
    print(sql)
    cur.close()

update("client", "test", {"a": "1", "b": "2"})

def insert(table, data):
    cur = conn.cursor()
    keys = data.keys()
    
    values = list(map(str, data.values()))
    sql = f"INSERT INTO {table} ({','.join(keys)}) VALUES ({','.join(values)});" 

    
    print(sql)
    cur.close()
    
insert("client", {"truc1": "bbbbb", "truc2": "aaaa"})