from fastapi import APIRouter, Query
from pydantic import BaseModel
from db import database as db

class Spread(BaseModel):
    data: dict


router = APIRouter()

# @router.get("/plots")
# async def get_plots(limit: int = Query(None, gt=0), desc: bool = False, asc: bool = True):
#     result = db.select("plot")

#     if not isinstance(result, dict) or 'results' not in result:
#         return {'error': 'Invalid data structure for plots'}

#     plots = result['results']
    
#     # Sorting logic based on 'desc' and 'asc'
#     key_to_sort_by = 'plot_number'
#     if desc:
#         plots = sorted(plots, key=lambda x: x.get(key_to_sort_by, 0), reverse=True)
#     elif asc:
#         plots = sorted(plots, key=lambda x: x.get(key_to_sort_by, 0))

#     # we verify the input for limit
#     if limit and limit > 0:
#         plots = plots[:limit]

#     return {'results': plots}

@router.get("/spread/{id_fertilizer}")
async def get_spread_by_id_fertilizer(id_fertilizer):
    """
        Get spread by id_fertilizer
        @param (int) id_fertilizer :  spread code
        @return (json) : Message of success or error
    """
    return db.select_one("spread", "id_fertilizer", id_fertilizer)

@router.post("/spread")
async def create_spread(spread: Spread):
    """
        Insert a new spread
        @param (Spread) spread : spread got in body
        @return (json) : Message of success or error
    """
    return db.insert("spread", spread.data)

@router.put("/spread/{id_fertilizer}")
async def replace_spread(id_fertilizer, spread: Spread):
    return db.update("spread", "id_fertilizer", id_fertilizer, spread.data)

@router.patch("/spread/{id_fertilizer}")
async def modify_spread(id_fertilizer, spread: Spread):
    return db.update("spread", "id_fertilizer", id_fertilizer, spread.data)

@router.delete("/spread/{id_fertilizer}")
async def delete_spread(id_fertilizer):
    """
        Delete spread by id_fertilizer
        @param (int) id_fertilizer :  id_fertilizer
        @return (json) : Message of success or error
    """
    return db.delete("spread", "id_fertilizer", id_fertilizer)