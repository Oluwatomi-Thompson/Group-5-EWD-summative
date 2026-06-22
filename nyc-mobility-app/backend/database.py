# backend/database.py

print("DATABASE.PY IS RUNNING SUCCESSFULLY")

import pandas as pd
import sqlite3
import os

DB_PATH = "nyc_taxi.db"


# ----------------------------
# CONNECT TO DATABASE
# ----------------------------
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


print("SCRIPT STARTED")


# ----------------------------
# CREATE TABLES
# ----------------------------
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Zones table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS taxi_zones (
        location_id INTEGER PRIMARY KEY,
        borough TEXT,
        zone TEXT,
        service_zone TEXT
    )
    """)

    # Trips table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trips (
        trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
        pickup_datetime TEXT,
        dropoff_datetime TEXT,
        trip_distance REAL,
        fare_amount REAL,
        total_amount REAL,
        passenger_count INTEGER,
        pu_location_id INTEGER,
        do_location_id INTEGER,
        trip_duration_minutes REAL,
        average_speed REAL,
        cost_per_mile REAL,
        pickup_geometry_type TEXT,
        dropoff_geometry_type TEXT
    )
    """)

    conn.commit()
    conn.close()


# ----------------------------
# LOAD SCHEMA (OPTIONAL)
# ----------------------------
def load_schema():
    conn = get_connection()
    cursor = conn.cursor()

    with open("backend/schema.sql", "r") as f:
        sql_script = f.read()

    cursor.executescript(sql_script)

    conn.commit()
    conn.close()
    print("Schema created successfully")


# ----------------------------
# LOAD ZONES DATA
# ----------------------------
def load_zones():
    conn = get_connection()
    cursor = conn.cursor()

    print("Loading zones data...")

    zones = pd.read_csv("../data/raw/taxi_zone_lookup.csv")

    for _, row in zones.iterrows():
        cursor.execute("""
            INSERT OR IGNORE INTO taxi_zones (
                location_id, borough, zone, service_zone
            )
            VALUES (?, ?, ?, ?)
        """, (
            row["LocationID"],
            row["Borough"],
            row["Zone"],
            row["service_zone"]
        ))

    conn.commit()
    conn.close()

    print(" Zones inserted properly")


# ----------------------------
# LOAD CLEANED TRIPS DATA
# ----------------------------
def load_trips():
    conn = get_connection()

    print("Loading cleaned dataset...")

    # Load cleaned data
    df = pd.read_parquet("../data/raw/yellow_tripdata.parquet")

    # ----------------------------
    # LIMIT DATA SIZE (CRITICAL FIX)
    # ----------------------------
    df = df.head(50000)
    print(f" Loaded {len(df)} rows")

    # ----------------------------
    # SAFETY CHECK
    # ----------------------------
    required_cols = [
        "trip_duration_minutes",
        "average_speed",
        "cost_per_mile",
        "pickup_geometry_type",
        "dropoff_geometry_type"
    ]

    for col in required_cols:
        if col not in df.columns:
            print(f"⚠ Missing column added: {col}")
            df[col] = 0

    # ----------------------------
    # RENAME COLUMNS
    # ----------------------------
    df = df.rename(columns={
        "PULocationID": "pu_location_id",
        "DOLocationID": "do_location_id",
        "tpep_pickup_datetime": "pickup_datetime",
        "tpep_dropoff_datetime": "dropoff_datetime"
    })

    # ----------------------------
    # FIX DATETIME (PREVENT SLOW INSERT)
    # ----------------------------
    if "pickup_datetime" in df.columns:
        df["pickup_datetime"] = df["pickup_datetime"].astype(str)

    if "dropoff_datetime" in df.columns:
        df["dropoff_datetime"] = df["dropoff_datetime"].astype(str)

    # ----------------------------
    # INSERT DATA (OPTIMIZED)
    # ----------------------------
    print(" Inserting trips into database...")

    df.to_sql(
        "trips",
        conn,
        if_exists="replace",
        index=False,
        chunksize=5000   # KEY FIX
    )

    conn.close()
    print(" Trips inserted successfully")


# ----------------------------
# RUN FULL PIPELINE
# ----------------------------
def run_pipeline():
    print(" Starting full pipeline...")

    create_tables()
    load_zones()
    load_trips()

    print(" Database setup complete")


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    run_pipeline()