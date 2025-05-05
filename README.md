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
5. Run the locally test using pytest
   ```
      pytest --cov=app --cov-report=html:coverage_report/html tests/ 
   ```
   
## How to run project using docker:
0. Install docker
1. Build the image locally
   ```
   docker build -t LOG_MONITORING .
   ```
2. Run the docker image created
   ```
   docker run -p 8000:8000 LOG_MONITORING
   ```

