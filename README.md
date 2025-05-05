# LSEG_LOG_MONITORING


## Prerequisites
    - python 3.11.9
    - Web Browser

## IDEE used:
    - PyCharm

## How to run project locally:
1. Open PyCharm
2. Install requirements.txt
    ```
        pip install -r requirements.txt
    ```
3. Run using uvicorn
    ```
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
4. Use the following link to interact with docs
    ```
    http://0.0.0.0:8000/docs
    ```