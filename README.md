# Apache airflow managment project 

This project is intended to organize all the ETL and ML procedures from various kind of projects. 

# Starting apache airflow

In separate terminals type: 

Starting webserver:

```
airflow webserver -p 8080
```

Starting task scheduler:

```
airflow scheduler
```

# DAGS 

The [D]irected [A]crylic [G]raphs are stored in the **dags/** directory. Dags are pipelines, which, when triggered, follows the defined steps in python scripts. 

## Vilnius-weather 

This project uses the 

