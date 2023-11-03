from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from db import database as db
from .user import get_current_user, User

class Production(BaseModel):
    
    """
    Represents a production.

    @param (dict) data: Dictionary containing data for the production.
    """

    data: dict


router = APIRouter()

@router.get("/productions")
async def get_production(limit: int = Query(None, gt=0),unit: str = None , desc: bool = False, asc: bool = True, current_user: User = Depends(get_current_user)):

    """
    Get a list of productions.

    @param (int) limit: Maximum number of productions to retrieve.
    @param (bool) desc: Sort in descending order.
    @param (bool) asc: Sort in ascending order.
    @param (User) current_user: Current user object obtained from dependency.

    @return (dict) : Dictionary containing a list of productions.
    """

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

    # Verify the input for limit
    if limit and limit > 0:
        production = production[:limit]
    
    # we verify the input for unit
    if unit:
        production = [x for x in production if x['unit'] == unit]

    return {'results': production}

@router.get("/productions/{production_code}")
async def get_production_by_production_code(production_code, current_user: User = Depends(get_current_user)):

    """
    Get production by production_code.

    @param (int) production_code :  production code.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """

    return db.select_one("production", "production_code", production_code)

@router.post("/productions")
async def create_production(production: Production, current_user: User = Depends(get_current_user)):

    """
    Insert a new production.

    @param (Production) production : production data.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """

    return db.insert("production", production.data)

@router.put("/productions/{production_code}")
async def replace_production(production_code, production: Production, current_user: User = Depends(get_current_user)):

    """
    Replace a production.

    @param (int) production_code: production code.
    @param (Production) production : production data.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """

    res = db.update("production", "production_code", production_code, production.data, {"pk_columns": ["production_code"], "columns": ["unit", "production_name"]})
    if "error_key" in res:
        db.conn.rollback()
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"You can not modify {res['error_key']} (primary key)"})
    return res


@router.patch("/productions/{production_code}")
async def modify_production(production_code, production: Production, current_user: User = Depends(get_current_user)):

    """
    Modify a production.

    @param (int) production_code: production code.
    @param (Production) production : production data.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """

    res =  db.update("production", "production_code", production_code, production.data, {"pk_columns": ["production_code"], "columns": []})
    if "error_key" in res:
        db.conn.rollback()
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"You can not modify {res['error_key']} (primary key)"})
    return res

@router.delete("/productions/{production_code}")
async def delete_production(production_code, current_user: User = Depends(get_current_user)):

    """
    Delete production by production_code.

    @param (int) production_code :  production_code.
    @return (json) : Message indicating success or error.
    """

    return db.delete("production", "production_code", production_code)
