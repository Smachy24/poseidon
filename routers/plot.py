from fastapi import APIRouter
from pydantic import BaseModel
from db import database as db

class Plot(BaseModel):
    data: dict


router = APIRouter()

@router.get("/plots")
async def get_plots():
    """
        Get all plots
        @return (json) : Message of success or error
    """
    return db.select("plot")

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