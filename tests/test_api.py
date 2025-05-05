from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)


def test_verify_root_of_application():
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert data == {"Hello": "LSEG"}


def test_log_monitoring_text_plain():
    # Sample log input
    test_log = (
        "11:35:00, scheduled task 001, START, 001\n"
        "11:40:30, scheduled task 001, END, 001\n"
    )
    response = client.post(
        "/log-monitoring/",
        files={"file": ("logs.txt", test_log, "text/plain")}
    )
    assert response.status_code == 404


def test_log_monitoring_upload_file():
    log_path = os.path.join("log", "logs.log")

    assert os.path.exists(log_path)

    with open(log_path, "rb") as f:
        response = client.post(
            "/log-interpretation/",
            files={"file": ("logs.log", f, "text/plain")}
        )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
