import requests # Allows access to requests library to call an API

BASE_URL = "https://api.openf1.org/v1"

def get_driver_standings(): # Grabs list of all drivers from latest F1 sessui, 
    url = f"{BASE_URL}/drivers?session_key=latest"
    response = requests.get(url)
    data = response.json()
    return data

def get_last_race_results(): # Grabs all positional changes throughout race
    url = f"{BASE_URL}/position?session_key=latest"
    response = requests.get(url)
    data = response.json()

    seen = {} # Filters above down to last position
    for entry in data:
        seen[entry["driver_number"]] = entry

    drivers = get_driver_standings() # Uses driver numbers to find details of driver - faster 
    driver_map = {d["driver_number"]: d for d in drivers}

    results = [] # Loops through above final positions to add names and teams
    for driver_number, entry in seen.items():
        driver_info = driver_map.get(driver_number, {})
        entry["full_name"] = driver_info.get("full_name", "Unknown")
        entry["team_name"] = driver_info.get("team_name", "Unknown")
        results.append(entry)

    results.sort(key=lambda x: x["position"]) # Sorts drivers by position to give a clear order 1-22
    return results

def get_driver_championship(): # Jolpica call for driver points... OpenF1's lack of this was an early oversight but easily rectified
    url = "https://api.jolpi.ca/ergast/f1/2026/driverStandings.json"
    response = requests.get(url)
    data = response.json()
    standings = data["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]
    return standings