from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from db import database as db
from .user import get_current_user, User

class Fertilizer(BaseModel):
    
    """
    Represents a fertilizer.

    @param (dict) data: Dictionary containing data for the fertilizer.
    """

    data: dict

router = APIRouter()

@router.get("/fertilizers")
async def get_fertilizers(limit: int = Query(None, gt=0),unit: str = None,  desc: bool = False, asc: bool = True, current_user: User = Depends(get_current_user)):

    """
    Get a list of fertilizers.

    @param (int) limit: Maximum number of fertilizers to retrieve.
    @param (bool) desc: Sort in descending order.
    @param (bool) asc: Sort in ascending order.
    @param (User) current_user: Current user object obtained from dependency.

    @return (dict) : Dictionary containing a list of fertilizers.
    """

    result = db.select("fertilizer")

    if not isinstance(result, dict) or 'results' not in result:
        return {'error': 'Invalid data structure for fertilizers'}

    fertilizers = result['results']
    
    # Sorting logic based on 'desc' and 'asc'
    key_to_sort_by = 'id_fertilizer'
    if desc:
        fertilizers = sorted(fertilizers, key=lambda x: x.get(key_to_sort_by, 0), reverse=True)
    elif asc:
        fertilizers = sorted(fertilizers, key=lambda x: x.get(key_to_sort_by, 0))

    # Verify the input for limit
    if limit and limit > 0:
        fertilizers = fertilizers[:limit]
        
    # we verify the input for unit
    if unit:
        fertilizers = [fertilizer for fertilizer in fertilizers if fertilizer['unit'] == unit]

    return {'results': fertilizers}

@router.get("/fertilizers/{id_fertilizer}")
async def get_fertilizer_by_id_fertilizer(id_fertilizer, current_user: User = Depends(get_current_user)):

    """
    Get fertilizer by id_fertilizer.

    @param (int) id_fertilizer : Fertilizer id.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """

    return db.select_one("fertilizer", "id_fertilizer", id_fertilizer)

@router.post("/fertilizers")
async def create_fertilizer(fertilizer: Fertilizer, current_user: User = Depends(get_current_user)):

    """
    Insert a new fertilizer.

    @param (Fertilizer) fertilizer : Fertilizer data.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """

    return db.insert("fertilizer", fertilizer.data)

@router.put("/fertilizers/{id_fertilizer}")
async def replace_fertilizer(id_fertilizer, fertilizer: Fertilizer, current_user: User = Depends(get_current_user)):

    """
    Replace a fertilizer.

    @param (int) id_fertilizer: Fertilizer id.
    @param (Fertilizer) fertilizer : Fertilizer data.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """

    res = db.update("fertilizer", "id_fertilizer", id_fertilizer, fertilizer.data, {"pk_columns": ["id_fertilizer"], "columns": ["unit", "production_name"]})
    if "error_key" in res:
        db.conn.rollback()
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"You can not modify {res['error_key']} (primary key)"})
    return res

@router.patch("/fertilizers/{id_fertilizer}")
async def modify_fertilizer(id_fertilizer, fertilizer: Fertilizer, current_user: User = Depends(get_current_user)):

    """
    Modify a fertilizer.

    @param (int) id_fertilizer: Fertilizer id.
    @param (Fertilizer) fertilizer : Fertilizer data.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """

    res =  db.update("fertilizer", "id_fertilizer", id_fertilizer, fertilizer.data, {"pk_columns": ["id_fertilizer"], "columns": []})
    if "error_key" in res:
        db.conn.rollback()
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"You can not modify {res['error_key']} (primary key)"})
    return res

@router.delete("/fertilizers/{id_fertilizer}")
async def delete_fertilizer(id_fertilizer, current_user: User = Depends(get_current_user)):

    """
    Delete fertilizer by id_fertilizer.

    @param (int) id_fertilizer : Fertilizer id.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """

    return db.delete("fertilizer", "id_fertilizer", id_fertilizer)
