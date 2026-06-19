from flask import Flask, jsonify
import sqlite3

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_PATH = "nyc_taxi.db"

print("APP LOADED SUCCESSFULLY")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return jsonify({"message": "NYC Taxi API is running"})


@app.route("/api/trips")
def get_trips():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM trips LIMIT 100")
    rows = cursor.fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


@app.route("/api/zones")
def get_zones():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM taxi_zones")
    rows = cursor.fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


@app.route("/api/analytics/top-boroughs")
def top_boroughs():
    conn = get_db()
    cursor = conn.cursor()

    query = """
    SELECT z.borough, COUNT(*) as total_trips
    FROM trips t
    JOIN taxi_zones z ON t.pu_location_id = z.location_id
    GROUP BY z.borough
    ORDER BY total_trips DESC
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


if __name__ == "__main__":
    print("STARTING FLASK SERVER...")
    app.run(debug=True)