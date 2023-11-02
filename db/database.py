import psycopg2
from db import constants
import datetime
from fastapi import HTTPException
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

        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'select_one' (Call {select_one_function_call_count}) called with parameters: {table, pk_column, pk_value}. Returned: {row_data}\n")


        return {"result": row_data}

    # Id must be a number
    except psycopg2.errors.InvalidTextRepresentation  as e:

        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'select_one' (Call {select_one_function_call_count}) encountered an error: {str(e)} de type {e.__class__.__name__}\n")
        
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"{pk_column} must be a number"})

    # Id does not exist
    except TypeError as e:
        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'select_one' (Call {select_one_function_call_count}) encountered an error: {str(e)} de type {e.__class__.__name__}\n")

        raise HTTPException(status_code=404, detail={"status" : "error","code": 404, "message": f"{pk_column} : {pk_value} does not exist"})

    except Exception as e:
        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'select_one' (Call {select_one_function_call_count}) encountered an error: {str(e)} de type {e.__class__.__name__}\n")

        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"An unexpected error has occurred"})

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
 

        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'insert' (Call {insert_function_call_count}) called with parameters: {table, data}. Returned: Succesfull \n")

        
        return {"status": "Sucess", "message": "Insertion successful"}

    # Primary key already exists
    except psycopg2.errors.UniqueViolation as e:

        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'select_one' (Call {select_one_function_call_count}) encountered an error: {str(e)} de type {e.__class__.__name__}\n")
        
        raise HTTPException(status_code=409, detail={"status" : "error","code": 409, "message": f"This primary key already exists", "description": e.pgerror})
    
    # Some fields does not exist
    except psycopg2.errors.UndefinedColumn as e:
        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'select_one' (Call {select_one_function_call_count}) encountered an error: {str(e)} de type {e.__class__.__name__}\n")
        
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"Columns are undefined", "description": e.pgerror})

    # Fields with constraint not null are empty
    except psycopg2.errors.NotNullViolation as e:
        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'select_one' (Call {select_one_function_call_count}) encountered an error: {str(e)} de type {e.__class__.__name__}\n")
        
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"One or many columns are missing", "description": e.pgerror})

    # Columns data types are incorrect
    except psycopg2.errors.DatatypeMismatch as e:
        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'select_one' (Call {select_one_function_call_count}) encountered an error: {str(e)} de type {e.__class__.__name__}\n")
        
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"One or many data types are incorrect", "description": e.pgerror})

    # Foreign key does not exist in table
    except psycopg2.errors.ForeignKeyViolation as e:
        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'select_one' (Call {select_one_function_call_count}) encountered an error: {str(e)} de type {e.__class__.__name__}\n")
        
        raise HTTPException(status_code=409, detail={"status" : "error","code": 409, "message": f"This foreign key does not exist", "description": e.pgerror})

    except Exception as e:
        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'select_one' (Call {select_one_function_call_count}) encountered an error: {str(e)} de type {e.__class__.__name__}\n")

        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"An unexpected error has occurred"})

    finally:
        cur.close()

def update(table, pk_column, pk_value, data):
    try:
        select_one(table, pk_column, pk_value)
    except:
       with open('agriculture.log', 'a') as log_file:
           current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           log_file.write(f"{current_time} - Function 'update' (Call {update_function_call_count}) called with parameters: {table, id, data}. Returned: Succesfull \n")
       select_one(table, pk_column, pk_value)
       
    try:
        cur = conn.cursor()
        
        update_columns = []
        for key in data.keys():
            update_columns.append(f"{key} = %s")

        conditions = ', '.join(update_columns)

        sql = f"UPDATE {table} SET {conditions} WHERE {pk_column} = %s;"
        cur.execute(sql, list(data.values()) + [pk_value])
        conn.commit()
      
        with open('agriculture.log', 'a') as log_file:
           current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           log_file.write(f"{current_time} - Function 'update' (Call {update_function_call_count}) called with parameters: {table, id, data}. Returned: Succesfull \n")
      
        return {"status": "Success", "message": "Update successful"}
   
     # Some fields does not exist
    except psycopg2.errors.UndefinedColumn as e:
        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'select_one' (Call {select_one_function_call_count}) encountered an error: {str(e)} de type {e.__class__.__name__}\n")
        
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"Columns are undefined", "description": e.pgerror})


    # Columns data types are incorrect
    except psycopg2.errors.DatatypeMismatch as e:
        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'select_one' (Call {select_one_function_call_count}) encountered an error: {str(e)} de type {e.__class__.__name__}\n")
        
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"One or many data types are incorrect", "description": e.pgerror})


    except Exception as e:
        error_result = {"error": str(e), "type": e.__class__.__name__}

        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'update' (Call {update_function_call_count}) encountered an error: {error_result}\n")

        return error_result

    finally:
        cur.close()



def delete(table, pk_column, pk_value):
    try:
        cur = conn.cursor()
        data = select_one(table, pk_column, pk_value)
        sql = f"DELETE FROM {table} WHERE {pk_column} = %s;"

        cur.execute(sql, [pk_value])
        conn.commit()
        
        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'delete' (Call {delete_function_call_count}) called with parameters: {table, id}. Returned: Succesfull \n")

        return {"status": "Sucess", "message": "Deletion successful"}

        
    except Exception as e:
        error_result = {"error": str(e), "type": e.__class__.__name__}
    
        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'delete' (Call {delete_function_call_count}) encountered an error: {error_result}\n")

        data = select_one(table, pk_column, pk_value)

    finally:
        cur.close()




    
