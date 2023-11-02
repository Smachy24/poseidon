from fastapi import APIRouter, Query
from pydantic import BaseModel
from db import database as db

class Production(BaseModel):
    data: dict


router = APIRouter()

@router.get("/productions")
async def get_production(limit: int = Query(None, gt=0), desc: bool = False, asc: bool = True):
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
    return db.update("production", "production_code", production_code, production.data)

@router.patch("/productions/{production_code}")
async def modify_production(production_code, production: Production):
    return db.update("production", "production_code", production_code, production.data)

@router.delete("/productions/{production_code}")
async def delete_production(production_code):
    """
        Delete production by production_code
        @param (int) production_code :  production_code
        @return (json) : Message of success or error
    """
    return db.delete("production", "production_code", production_code)