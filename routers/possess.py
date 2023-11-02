from fastapi import APIRouter, Query
from pydantic import BaseModel
from db import database as db

class Possess(BaseModel):
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

@router.get("/possess/{id_fertilizer}")
async def get_possess_by_id_fertilizer(id_fertilizer):
    """
        Get possess by id_fertilizer
        @param (int) id_fertilizer :  possess code
        @return (json) : Message of success or error
    """
    return db.select_one("possess", "id_fertilizer", id_fertilizer)

@router.post("/possess")
async def create_possess(possess: Possess):
    """
        Insert a new possess
        @param (Possess) possess : possess got in body
        @return (json) : Message of success or error
    """
    return db.insert("possess", possess.data)

@router.put("/possess/{id_fertilizer}")
async def replace_possess(id_fertilizer, possess: Possess):
    return db.update("possess", "id_fertilizer", id_fertilizer, possess.data)

@router.patch("/possess/{id_fertilizer}")
async def modify_possess(id_fertilizer, possess: Possess):
    return db.update("possess", "id_fertilizer", id_fertilizer, possess.data)

@router.delete("/possess/{id_fertilizer}")
async def delete_possess(id_fertilizer):
    """
        Delete possess by id_fertilizer
        @param (int) id_fertilizer :  id_fertilizer
        @return (json) : Message of success or error
    """
    return db.delete("possess", "id_fertilizer", id_fertilizer)