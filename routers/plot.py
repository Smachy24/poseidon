from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from db import database as db
from .user import get_current_user, User

class Plot(BaseModel):
    """
    Represents a plot.

    @param (dict) data: Dictionary containing data for the plot.
    """
    data: dict

router = APIRouter()

@router.get("/plots")
async def get_plots(limit: int = Query(None, gt=0), desc: bool = False, asc: bool = True, current_user: User = Depends(get_current_user)):
    """
    Get a list of plots.

    @param (int) limit: Maximum number of plots to retrieve.
    @param (bool) desc: Sort in descending order.
    @param (bool) asc: Sort in ascending order.
    @param (User) current_user: Current user object obtained from dependency.

    @return (dict) : Dictionary containing a list of plots.
    """
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

    # Verify the input for limit
    if limit and limit > 0:
        plots = plots[:limit]

    return {'results': plots}

@router.get("/plots/{plot_number}")
async def get_plot_by_plot_number(plot_number, current_user: User = Depends(get_current_user)):
    """
    Get plot by plot_number.

    @param (int) plot_number : Plot id.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """
    return db.select_one("plot", "plot_number", plot_number)

@router.post("/plots")
async def create_plot(plot: Plot, current_user: User = Depends(get_current_user)):
    """
    Insert a new plot.

    @param (Plot) plot : Plot data.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """
    return db.insert("plot", plot.data)

@router.put("/plots/{plot_number}")
async def replace_plot(plot_number, plot: Plot, current_user: User = Depends(get_current_user)):
    """
    Replace a plot.

    @param (int) plot_number: Plot id.
    @param (Plot) plot : Plot data.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """
    res = db.update("plot", "plot_number", plot_number, plot.data, {"pk_columns": ["plot_number"], "columns": ["unit", "production_name"]})
    if "error_key" in res:
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"You can not modify {res['error_key']} (primary key)"})
    return res

@router.patch("/plots/{plot_number}")
async def modify_plot(plot_number, plot: Plot, current_user: User = Depends(get_current_user)):
    """
    Modify a plot.

    @param (int) plot_number: Plot id.
    @param (Plot) plot : Plot data.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """
    res =  db.update("plot", "plot_number", plot_number, plot.data, {"pk_columns": ["plot_number"], "columns": []})
    if "error_key" in res:
        raise HTTPException(status_code=400, detail={"status" : "error","code": 400, "message": f"You can not modify {res['error_key']} (primary key)"})
    return res

@router.delete("/plots/{plot_number}")
async def delete_plot(plot_number, current_user: User = Depends(get_current_user)):
    """
    Delete plot by plot_number.

    @param (int) plot_number : Plot id.
    @param (User) current_user: Current user object obtained from dependency.

    @return (json) : Message indicating success or error.
    """
    return db.delete("plot", "plot_number", plot_number)
