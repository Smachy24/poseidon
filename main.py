from fastapi import FastAPI

from routers import plot, culture, date, unit, production, fertilizer, chimical_element, spread

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(plot.router)
app.include_router(culture.router)
app.include_router(date.router)
app.include_router(unit.router)
app.include_router(production.router)
app.include_router(fertilizer.router)
app.include_router(chimical_element.router)
app.include_router(spread.router)
