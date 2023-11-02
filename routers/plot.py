from fastapi import APIRouter, Query
from pydantic import BaseModel
from db import database as db

class Plot(BaseModel):
    data: dict


router = APIRouter()

@router.get("/plots")
async def get_plots(limit: int = Query(None, gt=0), desc: bool = False, asc: bool = True):
    result = db.select("plot")

    if not isinstance(result, dict) or 'results' not in result:
        return {'error': 'Invalid data structure for plots'}

    plots = result['results']
    
    # Sorting logic based on 'desc' and 'asc'
    key_to_sort_by = 'plot_number'
    if desc:
        plots = sorted(plots, key=lambda x: x.get(key_to_sort_by, 0), reverse=True)
    elif asc:
        plots = sorted(plots, key=lambda x: x.get(key_to_sort_by, 0))

    # we verify the input for limit
    if limit and limit > 0:
        plots = plots[:limit]

    return {'results': plots}

@router.get("/plots/{plot_number}")
async def get_plot_by_number(plot_number):
    """
        Get plot by plot_number
        @param (int) plot_number :  Plot number
        @return (json) : Message of success or error
    """
    return db.select_one("plot", "plot_number", plot_number)

@router.post("/plots")
async def create_plot(plot: Plot):
    """
        Insert a new plot
        @param (Plot) plot :  plot got in body
        @return (json) : Message of success or error
    """
    return db.insert("plot", plot.dict())

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