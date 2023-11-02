from fastapi import APIRouter, Query
from pydantic import BaseModel
from db import database as db

class Unit(BaseModel):
    data: dict


router = APIRouter()

@router.get("/units")
async def get_unit(limit: int = Query(None, gt=0)):
    result = db.select("unit")

    if not isinstance(result, dict) or 'results' not in result:
        return {'error': 'Invalid data structure for unit'}

    unit = result['results']

    # we verify the input for limit
    if limit and limit > 0:
        unit = unit[:limit]

    return {'results': unit}

@router.get("/units/{unit}")
async def get_unit_by_unit(unit):
    """
        Get unit by unit
        @param (int) unit :  unit
        @return (json) : Message of success or error
    """
    return db.select_one("unit", "unit", unit)

@router.post("/units")
async def create_unit(unit: Unit):
    """
        Insert a new unit
        @param (Unit) unit :  unit got in body
        @return (json) : Message of success or error
    """
    return db.insert("unit", unit.data)

@router.put("/units/{unit_value}")
async def replace_unit(unit_value, unit: Unit):
    return db.update("unit", "unit", unit_value, unit.data)

@router.patch("/units/{unit_value}")
async def modify_unit(unit_value, unit: Unit):
    return db.update("unit", "unit", unit_value, unit.data)

@router.delete("/units/{unit_value}")
async def delete_unit(unit_value):
    """
        Delete unit by unit value
        @param (str) unit_value :  unit value
        @return (json) : Message of success or error
    """
    return db.delete("unit", "unit", unit_value)