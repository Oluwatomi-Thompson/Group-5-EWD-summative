
# backend/models.py

from dataclasses import dataclass


@dataclass
class Trip:
    pickup_datetime: str
    dropoff_datetime: str
    trip_distance: float
    fare_amount: float
    total_amount: float
    passenger_count: int
    pu_location_id: int
    do_location_id: int
    trip_duration_minutes: float
    average_speed: float
    cost_per_mile: float


@dataclass
class Zone:
    location_id: int
    borough: str
    zone: str
    service_zone: str