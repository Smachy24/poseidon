from fastapi import APIRouter, HTTPException, Query, Depends

from pydantic import BaseModel
from db import database as db
from .user import get_current_user,User

class Culture(BaseModel):
    
    """
    Represents a culture.

    @param (dict) data: Dictionary containing data for the culture.
    """
        
    data: dict


router = APIRouter()

@router.get("/cultures")
async def get_culture(limit: int = Query(None, gt=0), quantity_harvested: int = Query(None, gt=0), desc: bool = False, asc: bool = True, current_user: User = Depends(get_current_user)):

    """
    Get a list of cultures.

    @param (int) limit: Maximum number of cultures to retrieve.
    @param (bool) desc: Sort in descending order.
    @param (bool) asc: Sort in ascending order.
    @param (User) current_user: Current user object obtained from dependency.

    @return (dict) : Dictionary containing a list of cultures.
    """

    result = db.select("culture")

    if not isinstance(result, dict) or 'results' not in result:
        return {'error': 'Invalid data structure for culture'}

    culture = result['results']
    
    # Sorting logic based on 'desc' and 'asc'
    key_to_sort_by = 'id_culture'
    if desc:
        culture = sorted(culture, key=lambda x: x.get(key_to_sort_by, 0), reverse=True)
    elif asc:
        culture = sorted(culture, key=lambda x: x.get(key_to_sort_by, 0))

    # we verify the input for limit
    if limit and limit > 0:
        culture = culture[:limit]
        
    # we verify the input for quantity_harvested
    if quantity_harvested and quantity_harvested > 0:
        culture = [x for x in culture if x['quantity_harvested'] >= quantity_harvested]

    return {'results': culture}

@router.get("/cultures/{id_culture}")
async def get_culture_by_id(id_culture, current_user: User = Depends(get_current_user)):
    """
        Get culture by id_culture
        @param (int) id_culture :  Culture id
        @return (json) : Message of success or error
    """
    return db.select_one("culture", "id_culture", id_culture)

@router.post("/cultures")
async def create_culture(culture: Culture, current_user: User = Depends(get_current_user)):
    """
        Insert a new culture
        @param (Culture) culture :  culture got in body
        @return (json) : Message of success or error
    """
    return db.insert("culture", culture.data)

@router.put("/cultures/{id_culture}")
async def replace_culture(id_culture, culture: Culture, current_user: User = Depends(get_current_user)):
    
    """
    Replace a culture.

    @param (int) id_culture: ID of the culture.
    @param (Culture) culture : Culture data.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """

    res = db.update("culture", "id_culture", id_culture, culture.data,{"pk_columns": ["id_culture"], "columns": ["plot_number", "production_code", "start_date", "end_date", "quantity_harvested"]})
    if "error_key" in res:
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"You can not modify {res['error_key']} (primary key)"})
    return res

@router.patch("/cultures/{id_culture}")
async def modify_culture(id_culture, culture: Culture, current_user: User = Depends(get_current_user)):

    """
    Modify a culture.

    @param (int) id_culture: ID of the culture.
    @param (Culture) culture : Culture data.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """
    
    res = db.update("culture", "id_culture", id_culture, culture.data, {"pk_columns": ["id_culture"], "columns": []})
    if "error_key" in res:
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"You can not modify {res['error_key']} (primary key)"})
    return res


@router.delete("/cultures/{id_culture}")
async def delete_culture(id_culture, current_user: User = Depends(get_current_user)):
    """
        Delete culture by id_culture
        @param (int) id_culture :  culture id
        @return (json) : Message of success or error
    """
    return db.delete("culture", "id_culture", id_culture)
