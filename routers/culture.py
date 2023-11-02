from fastapi import APIRouter, Query
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
async def get_plot_by_number(id_culture):
    """
        Get culture by id_culture
        @param (int) id_culture :  Culture id
        @return (json) : Message of success or error
    """
    return db.select_one("culture", "id_culture", id_culture)

@router.post("/cultures")
async def create_plot(culture: Culture):
    """
        Insert a new plot
        @param (Plot) plot :  plot got in body
        @return (json) : Message of success or error
    """
    return db.insert("culture", culture.data)

@router.put("/cultures/{id_culture}")
async def replace_plot(id_culture, culture: Culture):
    return db.update("culture", "id_culture", id_culture, culture.data)

@router.patch("/cultures/{id_culture}")
async def modify_plot(id_culture, culture: Culture):
    return db.update("culture", "id_culture", id_culture, culture.data)

@router.delete("/cultures/{id_culture}")
async def delete_plot(id_culture):
    """
        Delete plot by plot_number
        @param (int) plot_number :  Plot number
        @return (json) : Message of success or error
    """
    return db.delete("culture", "id_culture", id_culture)