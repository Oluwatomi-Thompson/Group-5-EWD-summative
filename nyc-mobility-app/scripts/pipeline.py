from clean_data import clean_data
from database import get_connection

# keep your existing imports
from schema import load_schema
from zones import load_zones


def load_trips(df):
    conn = get_connection()
    cur = conn.cursor()

    print("Clearing old trips...")
    cur.execute("DELETE FROM trips")

    print("Inserting cleaned trips...")

    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO trips (
                trip_id,
                pickup_datetime,
                dropoff_datetime,
                trip_distance,
                fare_amount,
                passenger_count,
                payment_type,
                pu_location_id,
                do_location_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row.get("trip_id"),
            row.get("tpep_pickup_datetime"),
            row.get("tpep_dropoff_datetime"),
            row.get("trip_distance"),
            row.get("fare_amount"),
            row.get("passenger_count"),
            row.get("payment_type"),
            row.get("PULocationID"),
            row.get("DOLocationID")
        ))

    conn.commit()
    conn.close()

    print("Trips inserted successfully")


def run_pipeline():
    print("PIPELINE STARTED")

    print("Creating schema...")
    load_schema()

    print("Loading zones...")
    load_zones()

    print("Running clean_data.py...")
    df = clean_data()   # 🔥 THIS CONNECTS YOUR CLEAN FILE

    print("Loading trips into database...")
    load_trips(df)      # 🔥 THIS CONNECTS TO DATABASE

    print("DATABASE SETUP COMPLETE")


if __name__ == "__main__":
    run_pipeline()