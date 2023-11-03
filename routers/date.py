from fastapi import APIRouter, Query, Depends
from pydantic import BaseModel
from datetime import datetime
from db import database as db
from .user import User,get_current_user

class Date(BaseModel):

    """
    Represents a date.

    @param (dict) data: Dictionary containing data for the date.
    """
        
    data: dict


router = APIRouter()

@router.get("/dates")
async def get_date(limit: int = Query(None, gt=0), desc: bool = False, asc: bool = True, current_user: User = Depends(get_current_user)):

    """
    Get a list of dates.

    @param (int) limit: Maximum number of dates to retrieve.
    @param (bool) desc: Sort in descending order.
    @param (bool) asc: Sort in ascending order.
    @param (User) current_user: Current user object obtained from dependency.

    @return (dict) : Dictionary containing a list of dates.
    """
     
    result = db.select("date")

    if not isinstance(result, dict) or 'results' not in result:
        return {'error': 'Invalid data structure for date'}

    date = result['results']
    
    # Sorting logic based on 'desc' and 'asc'
    key_to_sort_by = 'date'
    if desc:
        date = sorted(date, key=lambda x: x.get(key_to_sort_by, 0), reverse=True)
    elif asc:
        date = sorted(date, key=lambda x: x.get(key_to_sort_by, 0))

    # we verify the input for limit
    if limit and limit > 0:
        date = date[:limit]

    return {'results': date}

@router.get("/dates/{date}")
async def get_date_by_date(date, current_user: User = Depends(get_current_user)):
    """
        Get date by date
        @param (str) date :  Date
        @return (json) : Message of success or error
    """

    date = datetime.strptime(date, "%d-%m-%Y").date()
    date = date.strftime("%Y-%m-%d")
    return db.select_one("date", "date", date)

@router.post("/dates")
async def create_date(date: Date, current_user: User = Depends(get_current_user)):
    """
        Insert a new date
        @param (Date) date :  date got in body
        @return (json) : Message of success or error
    """

    date.data["date"] = datetime.strptime(date.data["date"], "%d-%m-%Y").date()
    date.data["date"] = date.data["date"].strftime("%Y-%m-%d")
    return db.insert("date", date.data)

@router.put("/dates/{date_value}")
async def replace_date(date_value, date: Date, current_user: User = Depends(get_current_user)):

    """
    Replace a date.

    @param (str) date_value: Date value.
    @param (Date) date : Date data.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """

    date.data["date"] = datetime.strptime(date.data["date"], "%d-%m-%Y").date()
    date.data["date"] = date.data["date"].strftime("%Y-%m-%d")

    date_value = datetime.strptime(date_value, "%d-%m-%Y").date()
    date_value = date_value.strftime("%Y-%m-%d")

    return db.update("date", "date", date_value, date.data, {"pk_columns": [], "columns": ["date"]})

@router.patch("/dates/{date_value}")
async def modify_date(date_value, date: Date, current_user: User = Depends(get_current_user)):

    """
    Modify a date.

    @param (str) date_value: Date value.
    @param (Date) date : Date data.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """
    
    date.data["date"] = datetime.strptime(date.data["date"], "%d-%m-%Y").date()
    date.data["date"] = date.data["date"].strftime("%Y-%m-%d")

    date_value = datetime.strptime(date_value, "%d-%m-%Y").date()
    date_value = date_value.strftime("%Y-%m-%d")
    return db.update("date", "date", date_value, date.data, {"pk_columns": [], "columns": ["date"]})

@router.delete("/dates/{date_value}")
async def delete_datet(date_value, current_user: User = Depends(get_current_user)):
    """
        Delete date by date
        @param (Date) date_value : Date
        @return (json) : Message of success or error
    """
    return db.delete("date", "date", date_value)