"""
Script cleans all the downloaded data 
"""
# Data wrangling 
import pandas as pd 

# Directory traversal 
import os 

# Configuration reading 
import yaml

# ENVIRON parameters
import dotenv

def clean_data_dirs():
    """
    Function that cleans all the directories with the downloaded data 
    """
    # Setting the current directory 
    _cur_dir = os.path.dirname(os.path.realpath(__file__))

    # Loading the environ params
    dotenv.load_dotenv(os.path.join(_cur_dir, '.env'))

    # Reading the configurations
    conf = conf = yaml.load(open(os.path.join(_cur_dir, "conf.yml"), encoding='utf8'), Loader=yaml.FullLoader)

    # Extracting the final subset of features
    features = conf.get("features_to_db")

    # Saving the path to data variable 
    _path_to_data = os.path.join(_cur_dir, 'data')

    # Listing all the dirs in the /data dir 
    dirs = os.listdir(_path_to_data)

    # Looping through all the dirs and aggregating data 
    for dir in dirs: 
        # Saving the directory name 
        _data_path = os.path.join(_path_to_data, dir)

        # Saving all the files in dir 
        _all_data = [os.path.join(_data_path, x) for x in os.listdir(_data_path)]
    
        # Removing the file with the ending **_agg.csv**
        _all_data = [x for x in _all_data if not x.endswith('_agg.csv')]

        # Reading all the files to a list of dfs
        _all_data_pd = [pd.read_csv(x) for x in _all_data]

        if len(_all_data_pd) > 0:

            # Concatenating all the data 
            _all_data_pd = pd.concat(_all_data_pd)

            # Getting the current feature list 
            features = list(set(features).intersection(set(_all_data_pd.columns)))

            # Aggregating by date 
            _all_data_pd = _all_data_pd.groupby('dt', as_index=False)[features].mean()

            # Saving to the current dir 
            _all_data_pd.to_csv(os.path.join(_data_path, 'data_agg.csv'), index=False)

            # Removing all the temporary data files 
            [os.remove(x) for x in _all_data]

if __name__ == '__main__':
    # Initiating the function 
    clean_data_dirs()