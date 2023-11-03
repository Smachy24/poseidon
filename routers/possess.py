from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from db import database as db
from .user import get_current_user, User

class Possess(BaseModel):
    """
    Represents a possess.

    @param (dict) data: Dictionary containing data for the possess.
    """
    data: dict

router = APIRouter()

@router.get("/possess")
async def get_possess(limit: int = Query(None, gt=0), desc: bool = False, asc: bool = True, current_user: User = Depends(get_current_user)):
    """
    Get a list of possess.

    @param (int) limit: Maximum number of possess to retrieve.
    @param (bool) desc: Sort in descending order.
    @param (bool) asc: Sort in ascending order.
    @param (User) current_user: Current user object obtained from dependency.

    @return (dict) : Dictionary containing a list of possess.
    """
    result = db.select("possess")

    if not isinstance(result, dict) or 'results' not in result:
        return {'error': 'Invalid data structure for possess'}

    possess = result['results']
    
    # Sorting logic based on 'desc' and 'asc'
    key_to_sort_by = 'id_fertilizer' # I keep id_fertilizer here
    if desc:
        possess = sorted(possess, key=lambda x: x.get(key_to_sort_by, 0), reverse=True)
    elif asc:
        possess = sorted(possess, key=lambda x: x.get(key_to_sort_by, 0))

    # Verify the input for limit
    if limit and limit > 0:
        possess = possess[:limit]

    return {'results': possess}

@router.get("/possess/{id_fertilizer}")
async def get_possess_by_id_fertilizer(id_fertilizer, current_user: User = Depends(get_current_user)):
    """
    Get possess by id_fertilizer.

    @param (int) id_fertilizer :  possess code.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """
    return db.select_one("possess", "id_fertilizer", id_fertilizer)

@router.post("/possess")
async def create_possess(possess: Possess, current_user: User = Depends(get_current_user)):
    """
    Insert a new possess.

    @param (Possess) possess : possess data.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """
    return db.insert("possess", possess.data)

@router.put("/possess/{id_fertilizer}")
async def replace_possess(id_fertilizer, possess: Possess, current_user: User = Depends(get_current_user)):
    """
    Replace a possess.

    @param (int) id_fertilizer: possess code.
    @param (Possess) possess : possess data.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """
    res =  db.update("possess", "id_fertilizer", id_fertilizer, possess.data, {"pk_columns": ["id_fertilizer", "element_code"], "columns": ["value"]})
    if "error_key" in res:
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"You can not modify {res['error_key']} (primary key)"})
    return res

@router.patch("/possess/{id_fertilizer}")
async def modify_possess(id_fertilizer, possess: Possess, current_user: User = Depends(get_current_user)):
    """
    Modify a possess.

    @param (int) id_fertilizer: possess code.
    @param (Possess) possess : possess data.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """
    res =  db.update("possess", "id_fertilizer", id_fertilizer, possess.data, {"pk_columns": ["id_fertilizer", "element_code"], "columns": []})
    if "error_key" in res:
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"You can not modify {res['error_key']} (primary key)"})
    return res

@router.delete("/possess/{id_fertilizer}")
async def delete_possess(id_fertilizer):
    """
    Delete possess by id_fertilizer.

    @param (int) id_fertilizer :  id_fertilizer.
    @return (json) : Message indicating success or error.
    """
    return db.delete("possess", "id_fertilizer", id_fertilizer)
