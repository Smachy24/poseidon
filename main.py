from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user,plot, culture, date, unit, production, fertilizer, chimical_element, spread, possess


app = FastAPI()

origins = [
    "http:10.57.35.82"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(user.router)
app.include_router(plot.router)
app.include_router(culture.router)
app.include_router(date.router)
app.include_router(unit.router)
app.include_router(production.router)
app.include_router(fertilizer.router)
app.include_router(chimical_element.router)
app.include_router(spread.router)
app.include_router(possess.router)
