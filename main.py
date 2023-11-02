from fastapi import FastAPI

from routers import plot
from routers import user

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(user.router)
app.include_router(plot.router)