
-- ============================
-- NYC TAXI MOBILITY DATABASE
-- Schema Design (Normalized)
-- ============================


-- ----------------------------
-- 1. DIMENSION TABLE: taxi_zones
-- ----------------------------
CREATE TABLE IF NOT EXISTS taxi_zones (
    location_id INTEGER PRIMARY KEY,
    borough TEXT NOT NULL,
    zone TEXT NOT NULL,
    service_zone TEXT
);


-- ----------------------------
-- 2. FACT TABLE: trips
-- ----------------------------
CREATE TABLE IF NOT EXISTS trips (
    trip_id INTEGER PRIMARY KEY AUTOINCREMENT,

    pickup_datetime TEXT NOT NULL,
    dropoff_datetime TEXT NOT NULL,

    pu_location_id INTEGER NOT NULL,
    do_location_id INTEGER NOT NULL,

    trip_distance REAL,
    fare_amount REAL,
    total_amount REAL,
    passenger_count INTEGER,

    trip_duration_minutes REAL,
    average_speed REAL,
    cost_per_mile REAL,

    pickup_geometry_type TEXT,
    dropoff_geometry_type TEXT,

    -- Foreign Key Constraints
    FOREIGN KEY (pu_location_id) REFERENCES taxi_zones(location_id),
    FOREIGN KEY (do_location_id) REFERENCES taxi_zones(location_id)
);


-- ----------------------------
-- 3. INDEXES (FOR PERFORMANCE)
-- ----------------------------

-- Speed up location-based queries
CREATE INDEX IF NOT EXISTS idx_trips_pu_location
ON trips (pu_location_id);

CREATE INDEX IF NOT EXISTS idx_trips_do_location
ON trips (do_location_id);

-- Speed up time-based analytics
CREATE INDEX IF NOT EXISTS idx_trips_pickup_time
ON trips (pickup_datetime);

-- Speed up distance/fare analysis
CREATE INDEX IF NOT EXISTS idx_trips_distance
ON trips (trip_distance);

CREATE INDEX IF NOT EXISTS idx_trips_fare
ON trips (fare_amount);