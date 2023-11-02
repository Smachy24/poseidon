from fastapi import FastAPI

from routers import plot, culture, date

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(plot.router)
app.include_router(culture.router)
app.include_router(date.router)