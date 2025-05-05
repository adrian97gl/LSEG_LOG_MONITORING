from fastapi import FastAPI, UploadFile, File, HTTPException
from starlette.responses import PlainTextResponse, Response
from utils.CONSTANTS import OUTPUTFILE
from app.monitor import Monitor
import os

app = FastAPI()


# There is the root of the application
@app.get("/")
async def root():
    return {"Hello": "LSEG"}


@app.post("/log-interpretation/", tags=["Log interpretation"])
async def log_monitoring(file: UploadFile = File(...)):
    if not file.filename.endswith(".log"):
        raise HTTPException(status_code=404, detail="Only .log files are supported.")

    contents = await file.read()
    lines = contents.decode("utf-8").split("\n")
    monitor = Monitor()
    result = monitor.log_monitor(lines)

    return result


@app.get("/observability", tags=["Observability"])
async def observability_report():
    report_path = 'log/' + OUTPUTFILE

    if not os.path.exists(report_path):
        return PlainTextResponse("No log file found.", status_code=404)

    with open(report_path, 'r') as file:
        contents = file.read()

    return contents
