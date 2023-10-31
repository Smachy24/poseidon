from fastapi import APIRouter, FastAPI

app = FastAPI()
router = APIRouter()


@router.get("/", tags=["test"])
async def read_root():
    return {"Hello": "World"}

app.include_router(router)