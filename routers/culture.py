from fastapi import APIRouter, Query, Depends
from pydantic import BaseModel
from db import database as db
from .user import get_current_user,User

class Culture(BaseModel):
    data: dict


router = APIRouter()

@router.get("/cultures")
async def get_culture(limit: int = Query(None, gt=0), desc: bool = False, asc: bool = True, current_user: User = Depends(get_current_user)):
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
    return db.update("culture", "id_culture", id_culture, culture.data)

@router.patch("/cultures/{id_culture}")
async def modify_culture(id_culture, culture: Culture, current_user: User = Depends(get_current_user)):
    return db.update("culture", "id_culture", id_culture, culture.data)

@router.delete("/cultures/{id_culture}")
async def delete_culture(id_culture, current_user: User = Depends(get_current_user)):
    """
        Delete culture by id_culture
        @param (int) id_culture :  culture id
        @return (json) : Message of success or error
    """
    return db.delete("culture", "id_culture", id_culture)