from fastapi import APIRouter, Query, Depends
from pydantic import BaseModel
from db import database as db
from .user import get_current_user, User

class Unit(BaseModel):

    """
    Represents a unit.

    @param (dict) data: Dictionary containing data for the unit.
    """

    data: dict


router = APIRouter()

@router.get("/units")
async def get_unit(limit: int = Query(None, gt=0), desc: bool = False, asc: bool = True, current_user: User = Depends(get_current_user)):
    
    """
    Get a list of units.

    @param (int) limit: Maximum number of units to retrieve.
    @param (bool) desc: Sort in descending order.
    @param (bool) asc: Sort in ascending order.
    @param (User) current_user: Current user object obtained from dependency.

    @return (dict) : Dictionary containing a list of units.
    """
    
    result = db.select("unit")

    if not isinstance(result, dict) or 'results' not in result:
        return {'error': 'Invalid data structure for unit'}

    unit = result['results']
    
    # Sorting logic based on 'desc' and 'asc'
    key_to_sort_by = 'unit'
    if desc:
        unit = sorted(unit, key=lambda x: x.get(key_to_sort_by, 0), reverse=True)
    elif asc:
        unit = sorted(unit, key=lambda x: x.get(key_to_sort_by, 0))

    # Verify the input for limit
    if limit and limit > 0:
        unit = unit[:limit]

    return {'results': unit}

@router.get("/units/{unit}")
async def get_unit_by_unit(unit, current_user: User = Depends(get_current_user)):

    """
    Get unit by unit.

    @param (str) unit :  unit.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """

    return db.select_one("unit", "unit", unit)

@router.post("/units")
async def create_unit(unit: Unit, current_user: User = Depends(get_current_user)):

    """
    Insert a new unit.

    @param (Unit) unit :  unit data.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """

    return db.insert("unit", unit.data)

@router.put("/units/{unit_value}")
async def replace_unit(unit_value, unit: Unit, current_user: User = Depends(get_current_user)):

    """
    Replace an existing unit.

    @param (str) unit_value: Unit value.
    @param (Unit) unit :  Unit data.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """

    return db.update("unit", "unit", unit_value, unit.data, {"pk_columns": [], "columns": ["unit"]})

@router.patch("/units/{unit_value}")
async def modify_unit(unit_value, unit: Unit, current_user: User = Depends(get_current_user)):

    """
    Modify an existing unit.

    @param (str) unit_value: Unit value.
    @param (Unit) unit :  Unit data.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """

    return db.update("unit", "unit", unit_value, unit.data, {"pk_columns": [], "columns": ["unit"]})

@router.delete("/units/{unit_value}")
async def delete_unit(unit_value, current_user: User = Depends(get_current_user)):

    """
    Delete unit by unit value.

    @param (str) unit_value :  Unit value.
    @return (json) : Message indicating success or error.
    """

    return db.delete("unit", "unit", unit_value)
