from fastapi import APIRouter, Query
from pydantic import BaseModel
from datetime import datetime
from db import database as db


class Date(BaseModel):
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

@router.get("/dates/{date}")
async def get_date_by_date(date):
    """
        Get date by date
        @param (int) date :  Date
        @return (json) : Message of success or error
    """

    date = datetime.strptime(date, "%d-%m-%Y").date()
    date = date.strftime("%Y-%m-%d")
    return db.select_one("date", "date", date)

@router.post("/dates")
async def create_date(date: Date):
    """
        Insert a new date
        @param (Plot) plot :  date got in body
        @return (json) : Message of success or error
    """

    date.data["date"] = datetime.strptime(date.data["date"], "%d-%m-%Y").date()
    date.data["date"] = date.data["date"].strftime("%Y-%m-%d")
    return db.insert("date", date.data)

@router.put("/dates/{date_value}")
async def replace_date(date_value, date: Date):
    date.data["date"] = datetime.strptime(date.data["date"], "%d-%m-%Y").date()
    date.data["date"] = date.data["date"].strftime("%Y-%m-%d")

    date_value = datetime.strptime(date_value, "%d-%m-%Y").date()
    date_value = date_value.strftime("%Y-%m-%d")

    return db.update("date", "date", date_value, date.data)

@router.patch("/dates/{date_value}")
async def modify_plot(date_value, date: Date):
    date.data["date"] = datetime.strptime(date.data["date"], "%d-%m-%Y").date()
    date.data["date"] = date.data["date"].strftime("%Y-%m-%d")

    date_value = datetime.strptime(date_value, "%d-%m-%Y").date()
    date_value = date_value.strftime("%Y-%m-%d")
    return db.update("date", "date", date_value, date.data)

@router.delete("/dates/{date_value}")
async def delete_plot(date_value):
    """
        Delete plot by plot_number
        @param (int) plot_number :  Plot number
        @return (json) : Message of success or error
    """
    return db.delete("date", "date", date_value)