from fastapi import FastAPI

from routers import customer

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(customer.router)