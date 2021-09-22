# Base image for apache
FROM apache/airflow:2.1.3-python3.8

# Installing additional packages
RUN pip install tensorflow==2.3.1 \
    && pip install python-dotenv==0.19.0 \
    && pip install pandas==1.3.0 \
    && pip install keras==2.4.3 \
    && pip install pydot==1.4.1 \
    && pip install requests==2.26.0 \
    && pip install SQLAlchemy==1.3.24 \
    && pip install psycopg2-binary==2.9.1 \
    && pip install tqdm==4.61.2