from fastapi import FastAPI, UploadFile, File, HTTPException
from starlette.responses import PlainTextResponse, HTMLResponse, JSONResponse
from app.utils.CONSTANTS import OUTPUTFILE
from app.monitor import Monitor
from app.processsimulator import ProcessSimulator
from prometheus_fastapi_instrumentator import Instrumentator

import os

app = FastAPI()

instrumentator = Instrumentator().instrument(app).expose(app)

# There is the root of the application
@app.get("/")
async def root():
    return {"Hello": "LSEG"}


@app.post("/log-interpretation/", tags=["Log interpretation"])
async def log_monitoring(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".log") and not file.filename.endswith(".csv"):
            raise HTTPException(status_code=404, detail="Only .csv / .log files are supported.")

        contents = await file.read()
        lines = contents.decode("utf-8").split("\n")
        monitor = Monitor()
        result = monitor.log_monitor(lines)

        return result
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong.")


@app.get("/observability", tags=["Observability"])
async def observability_report():
    try:
        report_path = 'log/' + OUTPUTFILE

        if not os.path.exists(report_path):
            return HTMLResponse("<p>No log file found.</p>", status_code=404)

        with open(report_path, 'r') as file:
            contents = file.read()

        html_content = f"<pre>{contents}</pre>"
        return HTMLResponse(content=html_content, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Something went wrong.")


@app.get("/simulate_logs", tags=["Simulate logs"])
async def simulate_logs(seconds: int):
    try:
        process_simulator = ProcessSimulator()
        result = process_simulator.start_process_simulator(seconds)

        return JSONResponse(content=result, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong. {e}")
