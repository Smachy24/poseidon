from fastapi import APIRouter

router = APIRouter()

@router.get("/customer")
async def get_customer():
    return {"customer" : "1"}