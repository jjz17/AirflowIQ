# AirflowIQ
Real-Time Air Quality Insights Data Pipeline

## Usage
### Initial Setup
1. (Download docker-compose file for airflow) ```curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.3.3/docker-compose.yaml'```
2. (Create project directories) ```mkdir -p ./dags ./logs ./plugins ./processed_data ./raw_data```
3. (Generate env file if using Linux, can skip for MacOS) ```echo -e "AIRFLOW_UID=$(id -u)" > .env```
4. (Set up virtual environment)
   1. ```python3 -m venv .venv```
   2. ```. .venv/bin/activate```
   3. ```pip install -r ./requirements.txt```
5. (Set up databases and create user account) ```docker-compose up airflow-init```

### General Setup
1. (Start all services) ```docker-compose up (optional -d flag)```
   1. (Monitor container health in another terminal window) ```docker ps```
2. Visit [airflow UI](http://localhost:8080) with default credentials (username/password): airflow/airflow
3. (Shut down all services) ```docker-compose down```
