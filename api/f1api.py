import requests

BASE_URL = "https://api.openf1.org/v1"

def get_driver_standings():
    url = f"{BASE_URL}/drivers?session_key=latest"
    response = requests.get(url)
    data = response.json()
    return data

def get_last_race_results():
    url = f"{BASE_URL}/position?session_key=latest"
    response = requests.get(url)
    data = response.json()
    return data

