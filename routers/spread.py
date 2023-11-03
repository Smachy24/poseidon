from fastapi import APIRouter, Query, Depends
from pydantic import BaseModel
from db import database as db
from .user import User,get_current_user

class Spread(BaseModel):
    data: dict


router = APIRouter()

@router.get("/spreads")
async def get_spread(limit: int = Query(None, gt=0),plot_number: int = Query(None, gt=0), desc: bool = False, asc: bool = True, current_user: User = Depends(get_current_user)):
    result = db.select("spread")

    if not isinstance(result, dict) or 'results' not in result:
        return {'error': 'Invalid data structure for spread'}

    spread = result['results']
    
    # Sorting logic based on 'desc' and 'asc'
    key_to_sort_by = 'id_fertilizer'  # I keep id_fertilizer here
    if desc:
        spread = sorted(spread, key=lambda x: x.get(key_to_sort_by, 0), reverse=True)
    elif asc:
        spread = sorted(spread, key=lambda x: x.get(key_to_sort_by, 0))

    # we verify the input for limit
    if limit and limit > 0:
        spread = spread[:limit]
        
    # we verify the input for plot_number
    if plot_number and plot_number > 0:
        spread = [s for s in spread if s['plot_number'] == plot_number]

    return {'results': spread}

@router.get("/spread/{id_fertilizer}")
async def get_spread_by_id_fertilizer(id_fertilizer, current_user: User = Depends(get_current_user)):
    """
        Get spread by id_fertilizer
        @param (int) id_fertilizer :  spread code
        @return (json) : Message of success or error
    """
    return db.select_one("spread", "id_fertilizer", id_fertilizer)

@router.post("/spread")
async def create_spread(spread: Spread, current_user: User = Depends(get_current_user)):
    """
        Insert a new spread
        @param (Spread) spread : spread got in body
        @return (json) : Message of success or error
    """
    return db.insert("spread", spread.data)

@router.put("/spread/{id_fertilizer}")
async def replace_spread(id_fertilizer, spread: Spread, current_user: User = Depends(get_current_user)):
    return db.update("spread", "id_fertilizer", id_fertilizer, spread.data)

@router.patch("/spread/{id_fertilizer}")
async def modify_spread(id_fertilizer, spread: Spread, current_user: User = Depends(get_current_user)):
    return db.update("spread", "id_fertilizer", id_fertilizer, spread.data)

@router.delete("/spread/{id_fertilizer}")
async def delete_spread(id_fertilizer, current_user: User = Depends(get_current_user)):
    """
        Delete spread by id_fertilizer
        @param (int) id_fertilizer :  id_fertilizer
        @return (json) : Message of success or error
    """
    return db.delete("spread", "id_fertilizer", id_fertilizer)