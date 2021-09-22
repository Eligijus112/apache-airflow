# Apache airflow managment project 

This project is intended to organize all the ETL and ML procedures from various kind of projects. 

# Starting apache airflow

Apache Airflow runs in docker following the official documentation. 

In separate terminals type: 

```
docker-compose up
```

To access the UI visit the link in the browser:

```
localhost:8080
```

USR: **airflow**
PSW: **airflow**

# DAGS 

The [D]irected [A]crylic [G]raphs are stored in the **dags/** directory. Dags are pipelines, which, when triggered, follows the defined steps in python scripts. 

## Vilnius-weather 

The project is in the **dags/Vilnius-weather** directory. Data is loaded from the **openweather** api and stored in an PSQL database. 

