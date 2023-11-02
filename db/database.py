import psycopg2
from db import constants
import datetime

# Connect to your postgres DB
conn = psycopg2.connect(f"dbname={constants.DBNAME} user={constants.USER} password={constants.PASSWORD}")

print("Connection réussie")


select_function_call_count = 0
select_one_function_call_count = 0
update_function_call_count = 0
delete_function_call_count = 0
insert_function_call_count = 0






def select(table):
    global select_function_call_count
    select_function_call_count += 1

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

        result = {"results": data}

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open('agriculture.log', 'a') as log_file:
            log_file.write(f"{current_time} - Function 'select' (Call {select_function_call_count}) called with parameters: {table}. Returned: {result}\n")

        return result

    except Exception as e:
        error_result = {"error": str(e)}

        with open('agriculture.log', 'a') as log_file:
            log_file.write(f"{current_time} - Function 'select' (Call {select_function_call_count}) encountered an error: {error_result}\n")

        return error_result

    finally:
        cursor.close()



def select_one(table, pk_column, pk_value):
    global select_one_function_call_count
    select_one_function_call_count += 1

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

        
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        with open('agriculture.log', 'a') as log_file:
            log_file.write(f"{current_time} - Function 'select_one' (Call {select_one_function_call_count}) called with parameters: {table, pk_column, pk_value}. Returned: {row_data}\n")


        return {"result": row_data}




    except Exception as e:
        error_result = {"error": str(e)}

        with open('agriculture.log', 'a') as log_file:
            log_file.write(f"{current_time} - Function 'select_one' (Call {select_one_function_call_count}) encountered an error: {error_result}\n")

        return error_result

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
        
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open('agriculture.log', 'a') as log_file:
            log_file.write(f"{current_time} - Function 'insert' (Call {insert_function_call_count}) called with parameters: {table, data}. Returned: Succesfull \n")

        
        return {"status": "Sucess", "message": "Insertion successful"}

    
    except Exception as e:
        error_result = {"error": str(e)}

        with open('agriculture.log', 'a') as log_file:
            log_file.write(f"{current_time} - Function 'insert' (Call {insert_function_call_count}) encountered an error: {error_result}\n")

        return error_result
        
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
      
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open('log/agriculture.log', 'a') as log_file:
           log_file.write(f"{current_time} - Function 'update' (Call {update_function_call_count}) called with parameters: {table, id, data}. Returned: Succesfull \n")
      
        return {"status": "Success", "message": "Update successful"}
    except Exception as e:
        error_result = {"error": str(e)}

        with open('log/agriculture.log', 'a') as log_file:
            log_file.write(f"{current_time} - Function 'update' (Call {update_function_call_count}) encountered an error: {error_result}\n")

        return error_result

    finally:
        cur.close()



def delete(table, pk_column, pk_value):
    try:
        cur = conn.cursor()
        sql = f"DELETE FROM {table} WHERE {pk_column} = %s;"
        cur.execute(sql, [pk_value])
        conn.commit()
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('log/agriculture.log', 'a') as log_file:
            log_file.write(f"{current_time} - Function 'delete' (Call {delete_function_call_count}) called with parameters: {table, id}. Returned: Succesfull \n")

        return {"status": "Sucess", "message": "Deletion successful"}

        
    except Exception as e:
        error_result = {"error": str(e)}

        with open('log/agriculture.log', 'a') as log_file:
            log_file.write(f"{current_time} - Function 'delete' (Call {delete_function_call_count}) encountered an error: {error_result}\n")

        return error_result

    finally:
        cur.close()




    
