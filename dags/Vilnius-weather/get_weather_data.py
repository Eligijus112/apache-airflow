# Date wrangling 
import datetime 
import time 
from datetime import timedelta

# Json parsing
import json

# Data wrangling 
import pandas as pd 

# Directory managment 
import os 

# Request making
import requests

# ENVIRON parameters
import dotenv

def get_weather_data():
    """
    Function that queries the free weather API from openweathermap.org and saves the response data
    """
    # Getting the current directory 
    cur_dir = os.path.dirname(os.path.realpath(__file__))

    # Reading the env parameters
    dotenv.load_dotenv(os.path.join(cur_dir, '.env'))

    # Getting the last 5 days worth of data 
    current_date = datetime.datetime.now()
    dates = [current_date - timedelta(x) for x in range(5)]

    # Iterating through the dates 
    df_hourly = pd.DataFrame({})

    for date in dates:
        # Converting to unix datetime 
        unix = int(time.mktime(date.date().timetuple()))

        # Making the request for Vilnius city weather data 
        req = requests.get(f"https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={54.7}&lon={25.3}&dt={unix}&appid={os.environ['API_KEY']}&units=metric")

        # Extracting the data from the response 
        response = json.loads(req.content)

        # Getting the hourly data 
        hourly = response.get('hourly')

        # Creating a tidy dataframe from the hourly data 
        df_hourly_date = pd.DataFrame([{
            "dt": x.get("dt"),
            "temp": x.get("temp"),
            "pressure": x.get('pressure'),
            "humidity": x.get('humidity'),
            "clouds": x.get("clouds"),
            "visibility": x.get('visibility'),
            "wind_speed": x.get('wind_speed'), 
            "wind_deg": x.get('wind_deg')
        } 
        for x in hourly
        ])

        # Appending to hourly df 
        df_hourly = pd.concat([df_hourly, df_hourly_date]) 

    # Converting unix date to datetime 
    df_hourly['dt'] = [datetime.datetime.fromtimestamp(x) for x in df_hourly['dt']]

    # Creating a folder to store the data in 
    _path_to_data = os.path.join(cur_dir, 'data', str(datetime.datetime.now().date()))

    try:
        os.mkdir(_path_to_data)
    except:
        print(f"Data folder {_path_to_data} already exists")

    # Saving the data to the folder 
    print(f"Downloaded number of rows: {df_hourly.shape[0]}")
    df_hourly.to_csv(f"{_path_to_data}/weather_data-{datetime.datetime.now()}.csv", index=False)

if __name__ == '__main__':
    # This section will only run if the script is called directly
    get_weather_data()