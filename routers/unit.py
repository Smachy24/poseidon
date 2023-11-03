from fastapi import APIRouter, Query
from pydantic import BaseModel
from db import database as db

class Unit(BaseModel):
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
    return db.update("unit", "unit", unit_value, unit.data, {"pk_columns": [], "columns": ["unit"]})

@router.patch("/units/{unit_value}")
async def modify_unit(unit_value, unit: Unit):
    return db.update("unit", "unit", unit_value, unit.data, {"pk_columns": [], "columns": ["unit"]})

@router.delete("/units/{unit_value}")
async def delete_unit(unit_value):
    """
        Delete unit by unit value
        @param (str) unit_value :  unit value
        @return (json) : Message of success or error
    """
    return db.delete("unit", "unit", unit_value)