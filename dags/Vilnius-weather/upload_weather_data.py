"""
Script that preproceses the raw weather data from the openweather API and writes it to the database
"""
# Data wrangling 
import pandas as pd 

# Directory traversal 
import os 

# Configuration reading 
import yaml

# Datetime wrangling 
from datetime import datetime

# Time tracking 
import time 

# ENVIRON parameters
import dotenv

# PSQL connection manager
import psycopg2

# Data engineering 
from data_engineering import sin_cos_hour, sin_cos_month

def upload_weather_data():
    """
    Function that uploads data to db 
    """
    # Setting the current directory 
    _cur_dir = os.path.dirname(os.path.realpath(__file__))

    # Loading the environ params
    dotenv.load_dotenv(os.path.join(_cur_dir, '.env'))

    # Reading the configurations
    conf = yaml.load(open(os.path.join(_cur_dir, "conf.yml"), encoding='utf8'), Loader=yaml.FullLoader)

    # Extracting the final subset of features
    features = conf.get("features_to_db")

    # Saving the name of the table for data upload 
    raw_data_table = conf.get('raw_data_table')

    # Listing all the directories in the data/ folder
    _data_folder = os.path.join(_cur_dir, "data")
    data_dirs = os.listdir(_data_folder)

    if len(data_dirs) > 0:
        # Creating an empty placeholder list for data 
        d = []

        # Reading through the folders and the files 
        for data_dir in data_dirs:
            # Defining the path 
            _data_paths = os.listdir(os.path.join(_data_folder, data_dir))

            # Leaving only .csv files
            _data_paths = [x for x in _data_paths if x.endswith("_agg.csv")]

            # Reading each file and leaving the predifined features
            if len(_data_paths) > 0:
                for _data_path in _data_paths:
                    data = pd.read_csv(os.path.join(_data_folder, data_dir, _data_path))

                    # Ensuring that every feature is present 
                    columns = set(data.columns)
                    missing_ft = set(features) - columns

                    for c in missing_ft:
                        data[c] = None

                    data = data[features]

                    # Appending to list 
                    d.append(data)
    
        # Concatenating all the data 
        d = pd.concat(d)

        # Grouping to avoid dublicates
        d = d.groupby('dt', as_index=False)[features].mean()
        d.reset_index(inplace=True, drop=True)

        # Preprocesing the datetime collumn 
        d['dt'] = [x.split(" +")[0] for x in d['dt']]
        d['dt'] = [datetime.strptime(x, "%Y-%m-%d %H:%M:%S") for x in d['dt']]

        # Creating additional features 
        hours = [sin_cos_hour(x) for x in d['dt']]
        month = [sin_cos_month(x) for x in d['dt']]

        hours = pd.DataFrame(hours)
        month = pd.DataFrame(month)

        # Saving to the original dataframe
        d[['hour_sin', 'hour_cos']] = hours[['hour_sin', 'hour_cos']]
        d[['month_sin', 'month_cos']] = month[['month_sin', 'month_cos']]

        # Making the connection to psql database
        conn = {}
        try:
            # Connection in docker
            conn = psycopg2.connect(
                host='weather_db',
                database=os.environ.get("POSTGRES_DB"),
                user=os.environ.get("POSTGRES_USER"),
                password=os.environ.get("POSTGRES_PASSWORD")
                )
        except:
            # Connection in local env 
            conn = psycopg2.connect(
                host=os.environ.get("POSTGRES_HOST"),
                database=os.environ.get("POSTGRES_DB"),
                user=os.environ.get("POSTGRES_USER"),
                password=os.environ.get("POSTGRES_PASSWORD"),
                port=os.environ.get("POSTGRES_PORT")
                )

        # TODO Change this behaviour to be a more elegant solution 
        # Droping data from the database 
        if isinstance(conn, psycopg2.extensions.connection):
            cursor = conn.cursor()
            cursor.execute(f"TRUNCATE {raw_data_table}")

            print(f"Total rows to db to be uploaded: {d.shape[0]}")

            start = time.time()
            
            # Copying the data 
            d.to_csv("temp.csv")
            with open('temp.csv', 'r') as f:
                next(f) # Skip the header row.
                cursor.copy_from(f, raw_data_table, sep=',')
            conn.commit()
            os.remove("temp.csv")

            print(f"Uploaded in: {round(time.time() - start, 4)} seconds")

if __name__ == "__main__":
    upload_weather_data()