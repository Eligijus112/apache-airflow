# Main deep learning lib 
from keras.models import Input, Model, Sequential
from keras.layers import Dense, LSTM
from keras import losses, optimizers

# Data wrangling 
import pandas as pd 

# Connection string reading 
import dotenv

# PSQL connection manager
import psycopg2

# Directory traversal
import os 

# Date wrangling 
import datetime 

# Scalers 
from sklearn.preprocessing import StandardScaler 

# Configuration reading 
import yaml

# Object serialization 
import pickle

def NN_model(
    X,
    Y,
    n_ahead,
    n_lag,
    batch_size,
    epochs, 
    lr,
    ):
    """
    Function that creates the deep learning model
    """
    # Defining the model architecture
    lstm_input = Input(shape=(n_lag, X.shape[1]))
    lstm_layer = LSTM(50, activation='relu')(lstm_input)
    x = Dense(n_ahead)(lstm_layer)

    model = Model(inputs=lstm_input, outputs=x)

    # Defining the optimizer 
    optimizer = optimizers.Adam(learning_rate=lr)

    # Compiling the model
    model.compile(loss=losses.MeanAbsoluteError(), optimizer=optimizer)

    # Fitting the model 
    model.fit(X, Y, batch_size, epochs)

    # Returning the model
    return model

def create_model():
    """
    Function that creates a deep learning model using raw Vilnius weather data; The model uses past 72 hour data to predict the next 24 hour data 
    """
    # Setting the current directory
    _cur_dir = os.path.dirname(os.path.realpath(__file__))

    # Saving the current run datetime 
    _cur_datetime = datetime.datetime.now()

    # Reading the env parameters
    dotenv.load_dotenv(os.path.join(_cur_dir, '.env'))

    # Reading the configurations
    conf = yaml.load(open(os.path.join(_cur_dir, "conf.yml"), encoding='utf8'), Loader=yaml.FullLoader)

    # Creating a directory to store the models
    _model_dir = os.path.join(_cur_dir, 'models')
    if not os.path.isdir(_model_dir):
        os.mkdir(_model_dir)

    # Creating the run directory
    _run_dir = os.path.join(_model_dir, _cur_datetime.strftime('%Y_%m_%d_%H_%M_%S'))
    if not os.path.isdir(_run_dir):
        os.mkdir(_run_dir)

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

    # Loading the modeling specific parameters
    NN_params = conf.get('NN_params')

    # Downloading data for modeling 
    d = pd.read_sql("select * from vilnius_weather_data", conn)

    # Creating the scalers
    features_to_scale = NN_params.get("features_to_scale")

    scalers = {}
    for feature_to_scale in features_to_scale:
        # Initiating an empty scaler 
        scaler = StandardScaler()

        # Fitting on data 
        scaler.fit(d[feature_to_scale].values.reshape(-1, 1))

        # Saving to dict 
        scalers[feature_to_scale] = scaler 

        # Scaling the data 
        d[feature_to_scale] = scaler.transform(d[feature_to_scale].values.reshape(-1, 1))

    # Saving the scaling artifact to the run dir 
    with open(os.path.join(_run_dir, "scalers.pkl"), 'wb') as f:
        pickle.dump(scalers, f, pickle.HIGHEST_PROTOCOL)

    # Calculating the difference between two datapoints
    d['date_diff'] = [x.seconds / 3600 for x in d['dt'].diff()]

    # Leaving only the features used in modeling 
    features = NN_params.get("features_to_use")
    d = d[features]

    # Saving the data artifact to a file 
    d.to_pickle(os.path.join(_run_dir, 'data.pkl'), index=False)
    
    # 


if __name__ == '__main__':
    create_model()