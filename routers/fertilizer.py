from fastapi import APIRouter, Query
from pydantic import BaseModel
from db import database as db

class Fertilizer(BaseModel):
    data: dict


router = APIRouter()

@router.get("/fertilizers")
async def get_fertilizers(limit: int = Query(None, gt=0), desc: bool = False, asc: bool = True):
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

    # we verify the input for limit
    if limit and limit > 0:
        fertilizers = fertilizers[:limit]

    return {'results': fertilizers}

@router.get("/fertilizers/{id_fertilizer}")
async def get_fertilizer_by_id_fertilizer(id_fertilizer):
    """
        Get fertilizer by id_fertilizer
        @param (int) id_fertilizer :  fertilizer id
        @return (json) : Message of success or error
    """
    return db.select_one("fertilizer", "id_fertilizer", id_fertilizer)

@router.post("/fertilizers")
async def create_fertilizer(fertilizer: Fertilizer):
    """
        Insert a new fertilizer
        @param (Fertilizer) fertilizer :  fertilizer got in body
        @return (json) : Message of success or error
    """
    return db.insert("fertilizer", fertilizer.data)

@router.put("/fertilizers/{id_fertilizer}")
async def replace_unit(id_fertilizer, fertilizer: Fertilizer):
    return db.update("fertilizer", "id_fertilizer", id_fertilizer, fertilizer.data)

@router.patch("/fertilizers/{id_fertilizer}")
async def modify_fertilizer(id_fertilizer, fertilizer: Fertilizer):
    return db.update("fertilizer", "id_fertilizer", id_fertilizer, fertilizer.data)

@router.delete("/fertilizers/{id_fertilizer}")
async def delete_fertilizer(id_fertilizer):
    """
        Delete fertilizer by id_fertilizer
        @param (int) id_fertilizer : fertilizer id
        @return (json) : Message of success or error
    """
    return db.delete("fertilizer", "id_fertilizer", id_fertilizer)