import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_earthquake_data(days=30, min_magnitude=2.5):
    """
    USGS Earthquake API se data fetch karta hai
    """
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)

    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": start_time.strftime("%Y-%m-%d"),
        "endtime": end_time.strftime("%Y-%m-%d"),
        "minmagnitude": min_magnitude,
        "orderby": "time"
    }

    print(f"Fetching earthquakes from last {days} days (magnitude >= {min_magnitude})...")
    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    features = data["features"]
    print(f"Total earthquakes found: {len(features)}")

    records = []
    for quake in features:
        props = quake["properties"]
        coords = quake["geometry"]["coordinates"]
        records.append({
            "time": pd.to_datetime(props["time"], unit="ms"),
            "place": props["place"],
            "magnitude": props["mag"],
            "depth_km": coords[2],
            "longitude": coords[0],
            "latitude": coords[1],
            "alert": props.get("alert", "none"),
            "tsunami": props.get("tsunami", 0),
            "type": props.get("type", "earthquake")
        })

    df = pd.DataFrame(records)
    df["date"] = df["time"].dt.date
    df["hour"] = df["time"].dt.hour
    df["magnitude_category"] = pd.cut(
        df["magnitude"],
        bins=[0, 3, 4, 5, 6, 10],
        labels=["Minor (2.5-3)", "Light (3-4)", "Moderate (4-5)", "Strong (5-6)", "Major (6+)"]
    )
    return df
