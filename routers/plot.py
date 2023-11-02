from fastapi import APIRouter, Query, Depends
from typing import Annotated
from pydantic import BaseModel
from db import database as db
from .user import get_current_user,User

class Plot(BaseModel):
    data: dict


router = APIRouter()

@router.get("/plots")
async def get_plots(limit: int = Query(None, gt=0), desc: bool = False, asc: bool = False, current_user: User = Depends(get_current_user)):
    result = db.select("plot")

    if not isinstance(result, dict) or 'results' not in result:
        return {'error': 'Invalid data structure for plots or is empty'}

    plots = result['results']
    
    # Sorting logic based on 'desc' and 'asc'
    key_to_sort_by = 'plot_number'
    
    # Handle case where we doesn't put any filters
    if asc == False and desc == False:
        asc = True
    
    if desc and asc:
        return{'error': "Only asc OR desc is possible to true"}
    elif desc:
        plots = sorted(plots, key=lambda x: x.get(key_to_sort_by, 0), reverse=True)
    elif asc:
        plots = sorted(plots, key=lambda x: x.get(key_to_sort_by, 0))

    # we verify the input for limit
    if limit and limit > 0:
        plots = plots[:limit]

    return {'results': plots}


@router.get("/plots/{plot_number}")
async def get_plot_by_number(plot_number, current_user: User = Depends(get_current_user)):
    return db.select_one("plot", "plot_number", plot_number)

@router.post("/plots")
async def create_plot(plot: Plot,current_user: User = Depends(get_current_user)):
    return db.insert("plot", plot.data)

@router.put("/plots/{plot_number}")
async def replace_plot(plot_number, plot: Plot):
    return db.update("plot", "plot_number", plot_number, plot.data)

@router.patch("/plots/{plot_number}")
async def modify_plot(plot_number, plot: Plot):
    return db.update("plot", "plot_number", plot_number, plot.data)

@router.delete("/plots/{plot_number}")
async def delete_plot(plot_number):
    """
        Delete plot by plot_number
        @param (int) plot_number :  Plot number
        @return (json) : Message of success or error
    """
    return db.delete("plot", "plot_number", plot_number)
