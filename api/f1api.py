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

    seen = {}
    for entry in data:
        seen[entry["driver_number"]] = entry

    drivers = get_driver_standings()
    driver_map = {d["driver_number"]: d for d in drivers}

    results = []
    for driver_number, entry in seen.items():
        driver_info = driver_map.get(driver_number, {})
        entry["full_name"] = driver_info.get("full_name", "Unknown")
        entry["team_name"] = driver_info.get("team_name", "Unknown")
        results.append(entry)

    results.sort(key=lambda x: x["position"])
    return results

def get_driver_championship():
    url = "https://api.jolpi.ca/ergast/f1/2026/driverStandings.json"
    response = requests.get(url)
    data = response.json()
    standings = data["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]
    return standings