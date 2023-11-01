from fastapi import FastAPI

from routers import plot

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(plot.router)