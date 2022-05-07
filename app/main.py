from fastapi import FastAPI

app = FastAPI(title="DataAPI")

@app.get("/")
def read_root():
    return {"hello": "world"}