import pandas as pd
import json

import os

os.makedirs("data/processed", exist_ok=True)

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




# Adding features

print("Calculating new features....")

# lst feature is the trip duration in minutes
time_difference = clean_trips['tpep_dropoff_datetime'] - clean_trips['tpep_pickup_datetime']
clean_trips['trip_duration_minutes'] = time_difference.dt.total_seconds() / 60.0

# fix: filter for any durations under 30 seconds to errors
clean_trips = clean_trips[clean_trips['trip_duration_minutes'] >= 0.5]
log_counts["dropped_zero_or_negative_durations"] = current_count - len(clean_trips)
current_count = len(clean_trips)

# 2nd feature is the average speed in mph
clean_trips['average_speed'] = clean_trips['trip_distance'] / (clean_trips['trip_duration_minutes'] / 60.0)

# fix: Filter out impossible speeds (max at 80 mph max)
clean_trips = clean_trips[clean_trips['average_speed'] <= 80.0]
log_counts["dropped_impossible_speeds"] = current_count - len(clean_trips)

# 3rd feature is the cost per mile
clean_trips['cost_per_mile'] = clean_trips['total_amount'] / clean_trips['trip_distance']


# adding spatial data

print("Integrating CSV and GeoJSON spatial metadata...")

# Map standard borough and zone names from the CSV file
clean_trips = pd.merge(clean_trips, zones, left_on='PULocationID', right_on='LocationID', how='left')
clean_trips = clean_trips.rename(columns={'Borough': 'pickup_borough', 'Zone': 'pickup_zone'}).drop(columns=['LocationID', 'service_zone'])

clean_trips = pd.merge(clean_trips, zones, left_on='DOLocationID', right_on='LocationID', how='left')
clean_trips = clean_trips.rename(columns={'Borough': 'dropoff_borough', 'Zone': 'dropoff_zone'}).drop(columns=['LocationID', 'service_zone'])

# fix:  a lookup mapping to remove spatial features  out of the  GeoJSON data
spatial_lookup = {}
for feature in geojson_data['features']:
    props = feature['properties']
    # Use standard fallback matching keys commonly found in TLC GeoJSON formats
    zone_id = props.get('LocationID') or props.get('objectid') or props.get('zone_id')
    if zone_id is not None:
        spatial_lookup[int(zone_id)] = str(feature['geometry']['type'])

#  map the geometric boundary type into  dataframe columns
clean_trips['pickup_geometry_type'] = clean_trips['PULocationID'].map(spatial_lookup)
clean_trips['dropoff_geometry_type'] = clean_trips['DOLocationID'].map(spatial_lookup)

# saving the results
print("Saving the final results....")
clean_trips.to_parquet("data/processed/cleaned_tripdata.parquet", index=False)

# fix: a structured log file containing exclusion reasons
log_counts["final_clean_records"] = len(clean_trips)
log_counts["total_records_excluded"] = total_raw_rows - len(clean_trips)

with open("data/processed/cleaning_log.json", "w") as log_file:
    json.dump(log_counts, log_file, indent=4)
print("Done, cleaned dataset and json logs are ready")