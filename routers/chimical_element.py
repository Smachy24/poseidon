from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from db import database as db

class ChimicalElement(BaseModel):
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

@router.get("/chimical-elements/{element_code}")
async def get_chimical_element_by_element_code(element_code):
    """
        Get chimical_element by element_code
        @param (int) element_code :  chimical_element id
        @return (json) : Message of success or error
    """
    return db.select_one("chimical_element", "element_code", element_code)

@router.post("/chimical-elements")
async def create_chimical_element(chimical_element: ChimicalElement):
    """
        Insert a new chimical_element
        @param (ChimicalElement) chimical_element :  chimical_element got in body
        @return (json) : Message of success or error
    """
    return db.insert("chimical_element", chimical_element.data)

@router.put("/chimical-elements/{element_code}")
async def replace_unit(element_code, chimical_element: ChimicalElement):
    res = db.update("chimical_element", "element_code", element_code, chimical_element.data, {"pk_columns": ["element_code"], "columns": ["unit", "wording_element"]})

    if "error_key" in res:
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"You can not modify {res['error_key']} (primary key)"})
    return res

@router.patch("/chimical-elements/{element_code}")
async def modify_chimical_element(element_code, chimical_element: ChimicalElement):
    res =  db.update("chimical_element", "element_code", element_code, chimical_element.data, {"pk_columns": ["element_code"], "columns": []})

    if "error_key" in res:
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"You can not modify {res['error_key']} (primary key)"})
    return res


@router.delete("/chimical-elements/{element_code}")
async def delete_chimical_element(element_code):
    """
        Delete chimical_element by element_code
        @param (int) element_code : chimical_element id
        @return (json) : Message of success or error
    """
    return db.delete("chimical_element", "element_code", element_code)