from fastapi import APIRouter, HTTPException, Query, Depends

from pydantic import BaseModel
from db import database as db
from .user import get_current_user,User
class Production(BaseModel):
    data: dict


router = APIRouter()

@router.get("/productions")
async def get_production(limit: int = Query(None, gt=0), desc: bool = False, asc: bool = True, current_user: User = Depends(get_current_user)):
    result = db.select("production")

    if not isinstance(result, dict) or 'results' not in result:
        return {'error': 'Invalid data structure for production'}

    production = result['results']
    
    # Sorting logic based on 'desc' and 'asc'
    key_to_sort_by = 'production_code'
    if desc:
        production = sorted(production, key=lambda x: x.get(key_to_sort_by, 0), reverse=True)
    elif asc:
        production = sorted(production, key=lambda x: x.get(key_to_sort_by, 0))

    # we verify the input for limit
    if limit and limit > 0:
        production = production[:limit]

    return {'results': production}

@router.get("/productions/{production_code}")
async def get_production_by_production_code(production_code, current_user: User = Depends(get_current_user)):
    """
        Get production by production_code
        @param (int) production_code :  production code
        @return (json) : Message of success or error
    """
    return db.select_one("production", "production_code", production_code)

@router.post("/productions")
async def create_production(production: Production, current_user: User = Depends(get_current_user)):
    """
        Insert a new production
        @param (Production) production : production got in body
        @return (json) : Message of success or error
    """
    return db.insert("production", production.data)

@router.put("/productions/{production_code}")
async def replace_production(production_code, production: Production, current_user: User = Depends(get_current_user)):
    return db.update("production", "production_code", production_code, production.data, {"pk_columns": ["production_code"], "columns": ["unit", "production_name"]})

@router.patch("/productions/{production_code}")
async def modify_production(production_code, production: Production, current_user: User = Depends(get_current_user)):
    res =  db.update("production", "production_code", production_code, production.data, {"pk_columns": ["production_code"], "columns": []})
    if "error_key" in res:
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"You can not modify {res['error_key']} (primary key)"})
    return res


@router.delete("/productions/{production_code}")
async def delete_production(production_code, current_user: User = Depends(get_current_user)):
    """
        Delete production by production_code
        @param (int) production_code :  production_code
        @return (json) : Message of success or error
    """
    return db.delete("production", "production_code", production_code)