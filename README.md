# AirflowIQ
Real-Time Air Quality Insights Data Pipeline

## What Problem does AirflowIQ Address?
Air quality affects the air we breathe. There are many factors that can lead to poor  air quality, but the two most common are related to elevated concentrations of ground-level ozone or particulate matter. Per EPA, ozone can cause a number of health problems, including coughing, breathing difficulty, and lung damage. Exposure to ozone can make the lungs more susceptible to infection, aggravate lung diseases, increase the frequency of asthma attacks, and increase the risk of early death from heart or lung disease. Similarly, particle pollution is linked to a number of health problems, including coughing, wheezing, reduced lung function, asthma attacks, heart attacks, strokes and even early death. 

This project aims to generate timely reports on air quality to inform people when their local air quality is unsafe, and they should remain indoors or take precautions to protect themselves.

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


### Data Sources
1. AirNow API (Air quality)
2. OpenWeatherMap (Not used yet)
3. tomorrow.io (Weather)
4. https://github.com/satellite-image-deep-learning/datasets