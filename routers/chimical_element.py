from fastapi import APIRouter, Query, Depends
from pydantic import BaseModel
from db import database as db
from .user import get_current_user,User

class ChimicalElement(BaseModel):
    data: dict


router = APIRouter()

@router.get("/chimical-elements")
async def get_chimical_element(limit: int = Query(None, gt=0),unit: str = None , desc: bool = False, asc: bool = True, current_user: User = Depends(get_current_user)):
    result = db.select("chimical_element")

    if not isinstance(result, dict) or 'results' not in result:
        return {'error': 'Invalid data structure for chimical_element'}

    chimical_element = result['results']
    
    # Sorting logic based on 'desc' and 'asc'
    key_to_sort_by = 'element_code'
    if desc:
        chimical_element = sorted(chimical_element, key=lambda x: x.get(key_to_sort_by, 0), reverse=True)
    elif asc:
        chimical_element = sorted(chimical_element, key=lambda x: x.get(key_to_sort_by, 0))

    # we verify the input for limit
    if limit and limit > 0:
        chimical_element = chimical_element[:limit]
        
    # we verify the input for unit
    if unit:
        chimical_element = [chimical_element for chimical_element in chimical_element if chimical_element['unit'] == unit]

    return {'results': chimical_element}

@router.get("/chimical-elements/{element_code}")
async def get_chimical_element_by_element_code(element_code, current_user: User = Depends(get_current_user)):
    """
        Get chimical_element by element_code
        @param (int) element_code :  chimical_element id
        @return (json) : Message of success or error
    """
    return db.select_one("chimical_element", "element_code", element_code)

@router.post("/chimical-elements")
async def create_chimical_element(chimical_element: ChimicalElement, current_user: User = Depends(get_current_user)):
    """
        Insert a new chimical_element
        @param (ChimicalElement) chimical_element :  chimical_element got in body
        @return (json) : Message of success or error
    """
    return db.insert("chimical_element", chimical_element.data)

@router.put("/chimical-elements/{element_code}")
async def replace_unit(element_code, chimical_element: ChimicalElement, current_user: User = Depends(get_current_user)):
    return db.update("chimical_element", "element_code", element_code, chimical_element.data)

@router.patch("/chimical-elements/{element_code}")
async def modify_chimical_element(element_code, chimical_element: ChimicalElement, current_user: User = Depends(get_current_user)):
    return db.update("chimical_element", "element_code", element_code, chimical_element.data)

@router.delete("/chimical-elements/{element_code}")
async def delete_chimical_element(element_code, current_user: User = Depends(get_current_user)):
    """
        Delete chimical_element by element_code
        @param (int) element_code : chimical_element id
        @return (json) : Message of success or error
    """
    return db.delete("chimical_element", "element_code", element_code)