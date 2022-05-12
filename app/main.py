from fastapi import FastAPI

from app.routers import api

app = FastAPI(title="DataAPI")
app.include_router(api.router)

@app.get("/")
def read_root():
    return {"hello": "world"}
