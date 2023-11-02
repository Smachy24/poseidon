import psycopg2
from db import constants

# Connect to your postgres DB
conn = psycopg2.connect(f"dbname={constants.DBNAME} user={constants.USER} password={constants.PASSWORD}")

print("Connection réussie")

def select(table):
    try:
        cursor = conn.cursor()
        query = f"SELECT * FROM {table};"
        cursor.execute(query)
        rows = cursor.fetchall()
        data = []

        column_names = [desc[0] for desc in cursor.description]

        for row in rows:
            row_data = {}
            for i in range(len(column_names)):
                column_name = column_names[i]
                column_value = row[i]
                row_data[column_name] = column_value
            data.append(row_data)

        return {"results": data}

    except Exception as e:
        return {"error": str(e)}

    finally:
        cursor.close()



def select_one(table, pk_column, pk_value):
    try:
        cursor = conn.cursor()
        query = f"SELECT * FROM {table} WHERE {pk_column} = %s;"
        cursor.execute(query, (pk_value,))
        result = cursor.fetchone()

        column_names = [desc[0] for desc in cursor.description]
        row_data = {}
        for i in range(len(column_names)):
            column_name = column_names[i]
            column_value = result[i]
            row_data[column_name] = column_value
        return {"result": row_data}


    except Exception as e:
        return {"error": str(e)}

    finally:
        cursor.close()


def insert(table, data):
    try:
        cur = conn.cursor()
        keys = data.keys()
        values = list(data.values())
        placeholders = ','.join(['%s'] * len(values))
        sql = f"INSERT INTO {table} ({','.join(keys)}) VALUES ({placeholders});"
         
        cur.execute(sql, values)
        conn.commit()
        return {"status": "Sucess", "message": "Insertion successful"}
    
    except Exception as e :
        return {"error": str(e)}
        
    finally:
        cur.close()

def update(table, pk_column, pk_value, data):
    try:
        cur = conn.cursor()
       
        update_columns = []
        for key in data.keys():
            update_columns.append(f"{key} = %s")

        conditions = ', '.join(update_columns)

        sql = f"UPDATE {table} SET {conditions} WHERE {pk_column} = %s;"
        cur.execute(sql, list(data.values()) + [pk_value])
        conn.commit()
        return {"status": "Success", "message": "Update successful"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cur.close()


def delete(table, pk_column, pk_value):
  
    try:
        cur = conn.cursor()
        sql = f"DELETE FROM {table} WHERE {pk_column} = %s;"
        cur.execute(sql, [pk_value])
        conn.commit()
        return {"status": "Sucess", "message": "Deletion successful"}
    except Exception as e :
         return {"error": str(e)}
            
    finally:
        cur.close()




    
