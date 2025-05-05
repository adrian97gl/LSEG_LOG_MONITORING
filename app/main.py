from fastapi import FastAPI

import os

app = FastAPI()


# There is the root of the application
@app.get("/")
async def root():
    return {"Hello": "LSEG"}
