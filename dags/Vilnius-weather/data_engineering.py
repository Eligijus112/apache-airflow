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

def create_X_Y(ts: np.array, lag=1, n_ahead=1, target_index=0) -> tuple:
    """
    A method to create X and Y matrix from a time series array for the training of 
    deep learning models 
    """
    # Extracting the number of features that are passed from the array 
    n_features = ts.shape[1]
    
    # Creating placeholder lists
    X, Y = [], []

    if len(ts) - lag <= 0:
        X.append(ts)
    else:
        for i in range(len(ts) - lag - n_ahead):
            Y.append(ts[(i + lag):(i + lag + n_ahead), target_index])
            X.append(ts[i:(i + lag)])

    X, Y = np.array(X), np.array(Y)

    # Reshaping the X array to an RNN input shape 
    X = np.reshape(X, (X.shape[0], lag, n_features))

    return X, Y