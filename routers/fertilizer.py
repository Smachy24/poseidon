from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from db import database as db

class Fertilizer(BaseModel):
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
    res = db.update("fertilizer", "id_fertilizer", id_fertilizer, fertilizer.data, {"pk_columns": ["id_fertilizer"], "columns": ["unit", "production_name"]})
    if "error_key" in res:
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"You can not modify {res['error_key']} (primary key)"})
    return res

@router.patch("/fertilizers/{id_fertilizer}")
async def modify_fertilizer(id_fertilizer, fertilizer: Fertilizer):
    res =  db.update("fertilizer", "id_fertilizer", id_fertilizer, fertilizer.data, {"pk_columns": ["id_fertilizer"], "columns": []})
    if "error_key" in res:
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"You can not modify {res['error_key']} (primary key)"})
    return res

@router.delete("/fertilizers/{id_fertilizer}")
async def delete_fertilizer(id_fertilizer):
    """
        Delete fertilizer by id_fertilizer
        @param (int) id_fertilizer : fertilizer id
        @return (json) : Message of success or error
    """
    return db.delete("fertilizer", "id_fertilizer", id_fertilizer)