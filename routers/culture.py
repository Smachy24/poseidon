from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from db import database as db

class Culture(BaseModel):
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

@router.get("/cultures/{id_culture}")
async def get_culture_by_id(id_culture):
    """
        Get culture by id_culture
        @param (int) id_culture :  Culture id
        @return (json) : Message of success or error
    """
    return db.select_one("culture", "id_culture", id_culture)

@router.post("/cultures")
async def create_culture(culture: Culture):
    """
        Insert a new culture
        @param (Culture) culture :  culture got in body
        @return (json) : Message of success or error
    """
    return db.insert("culture", culture.data)

@router.put("/cultures/{id_culture}")
async def replace_culture(id_culture, culture: Culture):
    res = db.update("culture", "id_culture", id_culture, culture.data,{"pk_columns": ["id_culture"], "columns": ["plot_number", "production_code", "start_date", "end_date", "quantity_harvested"]})
    if "error_key" in res:
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"You can not modify {res['error_key']} (primary key)"})
    return res

@router.patch("/cultures/{id_culture}")
async def modify_culture(id_culture, culture: Culture):
    res = db.update("culture", "id_culture", id_culture, culture.data, {"pk_columns": ["id_culture"], "columns": []})
    if "error_key" in res:
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"You can not modify {res['error_key']} (primary key)"})
    return res

@router.delete("/cultures/{id_culture}")
async def delete_culture(id_culture):
    """
        Delete culture by id_culture
        @param (int) id_culture :  culture id
        @return (json) : Message of success or error
    """
    return db.delete("culture", "id_culture", id_culture)
