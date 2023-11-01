from fastapi import APIRouter
from pydantic import BaseModel
from db import database as db

class Plot(BaseModel):
    plot_number: int
    surface: int
    plot_name: str
    coordinates: str

router = APIRouter()

@router.get("/plots")
async def get_plots():
    return db.select("plot")

@router.get("/plots/{plot_number}")
async def get_plot_by_number(plot_number):
    return db.select_one("plot", "plot_number", plot_number)

@router.post("/plots")
async def create_plot(plot: Plot):
    return db.insert("plot", plot.dict())