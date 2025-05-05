from fastapi import FastAPI

import os

app = FastAPI()


# There is the root of the application
@app.get("/")
async def root():
    return {"Hello": "LSEG"}


@app.post("/log-interpretation/", tags=["Log interpretation"])
async def log_interpretation():
    return {"Hello": "Log interpretation"}


@app.get("/observability", tags=["Observability"])
async def observability_report():
    return {"Hello": "Observability"}
