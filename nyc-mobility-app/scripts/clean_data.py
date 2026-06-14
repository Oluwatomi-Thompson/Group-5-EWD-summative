import pandas as pd
import json

# Load the raw data files
print("Loading files...")
trips = pd.read_parquet("data/raw/yellow_tripdata.parquet")
zones = pd.read_csv("data/raw/taxi_zone_lookup.csv")

# Open the geojson spatial file
with open("data/raw/taxi_zones.geojson", "r") as f:
    geojson_data = json.load(f)

# track the counts of the dropped rows for the technical report 
total_raw_rows = len(trips)
log_counts = {
    "total_raw_records": total_raw_rows,
    "dropped_missing_location_ids": 0,
    "dropped_invalid_distances": 0,
    "dropped_invalid_fares": 0,
    "dropped_zero_or_negative_durations": 0,
    "dropped_impossible_speeds": 0
}

# Cleannig the data

# Drop rows with missing or blank IDs
clean_trips = trips.dropna(subset=['PULocationID', 'DOLocationID'])
log_counts["dropped_missing_location_ids"] = total_raw_rows - len(clean_trips)
current_count = len(clean_trips)

# Convert time columns to actual datetime objects that can be used for calculations
clean_trips['tpep_pickup_datetime'] = pd.to_datetime(clean_trips['tpep_pickup_datetime'])
clean_trips['tpep_dropoff_datetime'] = pd.to_datetime(clean_trips['tpep_dropoff_datetime'])


clean_trips = clean_trips[(clean_trips['trip_distance'] > 0) & (clean_trips['trip_distance'] < 100)]
log_counts["dropped_invalid_distances"] = current_count - len(clean_trips)
current_count = len(clean_trips)

# Filtering the financials anomalies ( research show that the NYC minimum base fare standard is $2.50)
clean_trips = clean_trips[(clean_trips['fare_amount'] >= 2.50) & (clean_trips['total_amount'] >= 2.50)]
log_counts["dropped_invalid_fares"] = current_count - len(clean_trips)
current_count = len(clean_trips)