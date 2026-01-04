import json
import time
from datetime import datetime, timedelta
import requests




def save_dict_json(d, filename):
    """Save dictionary to JSON file"""
    with open(filename, 'w') as f:
        json.dump(d, f, indent=4)
    print(f"Saved to {filename}")

def load_dict_json(filename):
    """Load dictionary from JSON file"""
    with open(filename, 'r') as f:
        d = json.load(f)
    print(f"Loaded from {filename}")
    return d

config = load_dict_json("config.json")
access_token = config['access_token']

def my_task():
    """Your task to execute"""
    current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"Task executed at {current_time}")


def get_historical_data(instrument,start_date,end_date):
    url = f'https://api.upstox.com/v3/historical-candle/{instrument}/minutes/15/{end_date}/{start_date}'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    # Check the response status
    if response.status_code == 200:
        # Do something with the response data (e.g., print it)
        #@print(response.json())
        return response.json()
    else:
        # Print an error message if the request was not successful
        print("error from get_historical_data")
        print(f"Error: {response.status_code} - {response.text}")
        return None
    
def get_intraday_data(instrument):
    url = f'https://api.upstox.com/v3/historical-candle/intraday/{instrument}/minutes/15'
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)
    # Check the response status
    if response.status_code == 200:
        # Do something with the response data (e.g., print it)
        return response.json()
    else:
        # Print an error message if the request was not successful
        print('error from intraday historical data')
        print(f"Error: {response.status_code} - {response.text}")
        return None






