# Data wrangling 
import pandas as pd 

# Date wrangling
import datetime

# Array math 
import numpy as np

def sin_cos_hour(x: datetime.datetime) -> dict:
    """
    A function that creates sin and cos representation of the hour of day 
    """
    # Empty placeholder 
    sin_cos = {
        'hour_cos': np.nan, 
        'hour_sin': np.nan
    }

    if isinstance(x, datetime.datetime):

        # Extracting the hour of day
        hour = x.hour + 1

        # Extracting the sin and cos value on a daily cycle
        hour_cos = np.cos(hour * (2 * np.pi / 24))
        hour_sin = np.sin(hour * (2 * np.pi / 24))

        # Saving to dict 
        sin_cos['hour_cos'] = hour_cos
        sin_cos['hour_sin'] = hour_sin 

    # Returning the dict 
    return sin_cos
    
def sin_cos_month(x: datetime.datetime) -> dict:
    """
    A function that creates sin and cos representation of the month of year 
    """
    # Empty placeholder 
    sin_cos = {
        'month_cos': np.nan, 
        'month_sin': np.nan
    }

    if isinstance(x, datetime.datetime):

        # Extracting the hour of day
        month = x.month

        # Extracting the sin and cos value on a daily cycle
        month_cos = np.cos(month * (2 * np.pi / 12))
        month_sin = np.sin(month * (2 * np.pi / 12))

        # Saving to dict 
        sin_cos['month_cos'] = month_cos
        sin_cos['month_sin'] = month_sin 

    # Returning the dict 
    return sin_cos