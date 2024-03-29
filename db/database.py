import psycopg2
from db import constants
import datetime
from fastapi import HTTPException
# Connect to your postgres DB
conn = psycopg2.connect(f"host={constants.HOST},dbname={constants.DBNAME} user={constants.USER} password={constants.PASSWORD}")

print("Connection réussie")


select_function_call_count = 0
select_one_function_call_count = 0
update_function_call_count = 0
delete_function_call_count = 0
insert_function_call_count = 0






def select(table):
    
    """
    Retrieve all records from the specified table.

    @param (str) table : The name of the table to select records from.
    @return (dict) : A dictionary containing the selected records.
    """

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
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'select' (Call {select_function_call_count}) encountered an error: {error_result}\n")

        return error_result

    finally:
        cursor.close()



def select_one(table, pk_column, pk_value):

    """
    Retrieve a single record from the specified table based on the primary key.

    @param (str) table : The name of the table to select the record from.
    @param (str) pk_column : The primary key column name.
    @param pk_value : The value of the primary key to identify the record.

    @return (dict) : A dictionary containing the selected record.
    """

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

    """
    Insert a new record into the specified table.

    @param (str) table : The name of the table to insert the record into.
    @param (dict) data : A dictionary containing the data to be inserted.

    @return (dict) : A success message upon successful insertion.
    """

    global insert_function_call_count
    insert_function_call_count += 1
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

    except psycopg2.errors.SyntaxError as e:
        conn.rollback()
        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'select_one' (Call {update_function_call_count}) encountered an error: {str(e)} de type {e.__class__.__name__}\n")
        
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"Data must not be empty"})


    # Primary key already exists
    except psycopg2.errors.UniqueViolation as e:
        conn.rollback()
        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'select_one' (Call {insert_function_call_count}) encountered an error: {str(e)} de type {e.__class__.__name__}\n")
        
        raise HTTPException(status_code=409, detail={"status" : "error","code": 409, "message": f"This primary key already exists", "description": e.pgerror})
    
    # Some fields does not exist
    except psycopg2.errors.UndefinedColumn as e:
        conn.rollback()
        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'select_one' (Call {insert_function_call_count}) encountered an error: {str(e)} de type {e.__class__.__name__}\n")
        
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"Columns are undefined", "description": e.pgerror})

    # Fields with constraint not null are empty
    except psycopg2.errors.NotNullViolation as e:
        conn.rollback()
        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'select_one' (Call {insert_function_call_count}) encountered an error: {str(e)} de type {e.__class__.__name__}\n")
        
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"One or many columns are missing", "description": e.pgerror})

    # Columns data types are incorrect
    except psycopg2.errors.DatatypeMismatch as e:
        conn.rollback()
        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'select_one' (Call {insert_function_call_count}) encountered an error: {str(e)} de type {e.__class__.__name__}\n")
        
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"One or many data types are incorrect", "description": e.pgerror})

    # Foreign key does not exist in table
    except psycopg2.errors.ForeignKeyViolation as e:
        conn.rollback()
        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'select_one' (Call {insert_function_call_count}) encountered an error: {str(e)} de type {e.__class__.__name__}\n")
        
        raise HTTPException(status_code=409, detail={"status" : "error","code": 409, "message": f"This foreign key does not exist", "description": e.pgerror})

    except Exception as e:
        conn.rollback()
        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'select_one' (Call {insert_function_call_count}) encountered an error: {str(e)} de type {e.__class__.__name__}\n")

        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"An unexpected error has occurred"})

    finally:
        cur.close()

def update(table, pk_column_where, pk_value, data, columns={"pk_columns": [], "columns": []}):

    """
    Update an existing record in the specified table.

    @param (str) table : The name of the table to update the record in.
    @param (str) pk_column_where : The primary key column name for identifying the record.
    @param pk_value : The value of the primary key to identify the record.
    @param (dict) data : A dictionary containing the updated data.
    @param (dict) columns : A dictionary specifying primary key columns and other columns to be modified.

    @return (dict) : A success message upon successful update.
    """

    global update_function_call_count
    update_function_call_count += 1
    try:
        select_one(table, pk_column_where, pk_value)
    except:
       conn.rollback()
       with open('agriculture.log', 'a') as log_file:
           current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           log_file.write(f"{current_time} - Function 'update' (Call {update_function_call_count}) called with parameters: {table, id, data}. Returned: Succesfull \n")
       select_one(table, pk_column_where, pk_value)
    
    if not all(a in data.keys() for a in columns["columns"]):
        conn.rollback()
        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'select_one' (Call {update_function_call_count}) encountered an error: You must modify all the keys: {columns['columns']} de type Exception\n")
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"You must modify all these columns : {columns['columns']}"})

    try:
        cur = conn.cursor()
        
        update_columns = []
        for key in data.keys():
            if key in columns["pk_columns"]:
                with open('agriculture.log', 'a') as log_file:
                    conn.rollback()
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_file.write(f"{current_time} - Function 'select_one' (Call {update_function_call_count}) encountered an error: {f'You can not modify {key} (primary key)'} de type Exception\n")
                return {"error_key":key}
            update_columns.append(f"{key} = %s")

  

        conditions = ', '.join(update_columns)

        sql = f"UPDATE {table} SET {conditions} WHERE {pk_column_where} = %s;"
        cur.execute(sql, list(data.values()) + [pk_value])
        conn.commit()
      
        with open('agriculture.log', 'a') as log_file:
           current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           log_file.write(f"{current_time} - Function 'update' (Call {update_function_call_count}) called with parameters: {table, id, data}. Returned: Succesfull \n")
      
        return {"status": "Success", "message": "Update successful"}
   
    except psycopg2.errors.SyntaxError as e:
        conn.rollback()
        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'select_one' (Call {update_function_call_count}) encountered an error: {str(e)} de type {e.__class__.__name__}\n")
        
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"Data must not be empty"})

     # Some fields does not exist
    except psycopg2.errors.UndefinedColumn as e:
        conn.rollback()
        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'select_one' (Call {update_function_call_count}) encountered an error: {str(e)} de type {e.__class__.__name__}\n")
        
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"Columns are undefined", "description": e.pgerror})


    # Columns data types are incorrect
    except psycopg2.errors.DatatypeMismatch as e:
        conn.rollback()
        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'select_one' (Call {update_function_call_count}) encountered an error: {str(e)} de type {e.__class__.__name__}\n")
        
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"One or many data types are incorrect", "description": e.pgerror})

    # Foreign key does not exist in table
    except psycopg2.errors.ForeignKeyViolation as e:
        conn.rollback()
        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'select_one' (Call {update_function_call_count}) encountered an error: {str(e)} de type {e.__class__.__name__}\n")
        
        raise HTTPException(status_code=409, detail={"status" : "error","code": 409, "message": f"This foreign key does not exist", "description": e.pgerror})

    

    except Exception as e:
        conn.rollback()
        error_result = {"error": str(e), "type": e.__class__.__name__}

        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'update' (Call {update_function_call_count}) encountered an error: {error_result}\n")

        return error_result

    finally:
        cur.close()



def delete(table, pk_column, pk_value):

    """
    Delete a record from the specified table based on the primary key.

    @param (str) table : The name of the table to delete the record from.
    @param (str) pk_column : The primary key column name.
    @param pk_value : The value of the primary key to identify the record.

    @return (dict) : A success message upon successful deletion.
    """

    global delete_function_call_count
    delete_function_call_count += 1
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
        conn.rollback()
        error_result = {"error": str(e), "type": e.__class__.__name__}
    
        with open('agriculture.log', 'a') as log_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{current_time} - Function 'delete' (Call {delete_function_call_count}) encountered an error: {error_result}\n")

        data = select_one(table, pk_column, pk_value)

    finally:
        cur.close()




    
