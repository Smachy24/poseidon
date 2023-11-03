from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from db import database as db

class Production(BaseModel):
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

@router.get("/productions/{production_code}")
async def get_production_by_production_code(production_code):
    """
        Get production by production_code
        @param (int) production_code :  production code
        @return (json) : Message of success or error
    """
    return db.select_one("production", "production_code", production_code)

@router.post("/productions")
async def create_production(production: Production):
    """
        Insert a new production
        @param (Production) production : production got in body
        @return (json) : Message of success or error
    """
    return db.insert("production", production.data)

@router.put("/productions/{production_code}")
async def replace_production(production_code, production: Production):
    return db.update("production", "production_code", production_code, production.data, {"pk_columns": ["production_code"], "columns": ["unit", "production_name"]})

@router.patch("/productions/{production_code}")
async def modify_production(production_code, production: Production):
    res =  db.update("production", "production_code", production_code, production.data, {"pk_columns": ["production_code"], "columns": []})
    if "error_key" in res:
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"You can not modify {res['error_key']} (primary key)"})
    return res

@router.delete("/productions/{production_code}")
async def delete_production(production_code):
    """
        Delete production by production_code
        @param (int) production_code :  production_code
        @return (json) : Message of success or error
    """
    return db.delete("production", "production_code", production_code)