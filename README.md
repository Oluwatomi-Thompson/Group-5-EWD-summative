# NYC Urban Mobility Dashboard 


# Video Walkthrough
Access the video walkthrough for detailed instructions here:
https://youtu.be/EABbpghFh-0


# Overview

The NYC Urban Mobility Dashboard is a full-stack data analytics application developed for the Enterprise Web Development Summative Project. It processes real-world NYC Taxi Trip data and presents meaningful insights through an interactive dashboard.

The system demonstrates a complete data pipeline — from raw dataset ingestion and cleaning to database storage, API development, and frontend visualization.


# Objectives

* Clean and preprocess raw NYC taxi data
* Store structured data in a relational database
* Build a backend API for data access
* Create an interactive dashboard for data exploration
* Generate meaningful insights from urban mobility data


# Features

* Responsive user interface
* Interactive dashboard with real-time data
* Data visualization using Chart.js
* Flask REST API integration
* SQLite database storage
* Data cleaning and preprocessing pipeline
* Summary statistics (trips, fare, distance)
* Dynamic data fetching using Fetch API



# System Architecture

# Components:

* **Data Processing Layer** → `clean_data.py`
* **Pipeline Execution** → `pipeline.py`
* **Database Layer** → SQLite (`nyc_taxi.db`)
* **Backend API** → Flask (`app.py`)
* **Frontend Dashboard** → HTML, CSS, JavaScript


# Project Structure

```bash
Group-5-EWD-summative/
│
├── backend/
│   ├── app.py
│   ├── schema.sql
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── dashboard.html
│   ├── css/
│   ├── js/
│   └── images/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── scripts/
│   ├── clean_data.py
│   ├── pipeline.py
│   ├── database.py
│   └── dsa_ranking.py
│
├── .gitignore
└── README.md
```

# Dataset

This project uses the NYC Yellow Taxi Trip dataset from the New York City Taxi and Limousine Commission (TLC).

# Data includes:

* Pickup and drop-off locations
* Trip distance and duration
* Fare and total cost
* Passenger count
* Payment method



# Data Processing & Cleaning

Data is cleaned using `clean_data.py`:

# Cleaning Steps:

* Removed missing location IDs
* Filtered invalid distances and fares
* Removed unrealistic speeds (> 80 mph)
* Converted timestamps to proper datetime format
* Removed extremely short or invalid trips

# Feature Engineering:

* Trip Duration (minutes)
* Average Speed (mph)
* Cost per Mile


# Database Design

SQLite database (`nyc_taxi.db`) stores processed data.

# Table: `trips`

| Column           | Description            |
| ---------------- | ---------------------- |
| trip_id          | Unique trip identifier |
| pickup_datetime  | Trip start time        |
| dropoff_datetime | Trip end time          |
| trip_distance    | Distance (miles)       |
| fare_amount      | Fare cost              |
| passenger_count  | Number of passengers   |
| payment_type     | Payment method         |
| pu_location_id   | Pickup location        |
| do_location_id   | Dropoff location       |

---

# Setup Instructions

# 1. Clone Repository

```bash
git clone https://github.com/Oluwatomi-Thompson/Group-5-EWD-summative.git
cd Group-5-EWD-summative
```

---

# 2. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

---

# 3. Run Data Pipeline

```bash
python scripts/pipeline.py
```

This step:

* Cleans raw dataset
* Generates processed data
* Populates the database

---

### 4. Start Backend Server

```bash
cd backend
python app.py
```

Server runs at:

```
http://127.0.0.1:5000
```

---

# 5. Run Frontend

Open the frontend using Live Server or open `index.html` in your browser.



#  API Endpoints

# GET `/api/trips`

Returns trip records used in the dashboard and chart


# Dashboard Features

* Trip records table
* Search and filtering functionality
* Summary statistics:

  * Total Trips
  * Average Fare
  * Average Distance
* Payment method distribution chart


# Visualizations

# Payment Distribution Chart

Shows distribution of:

* Cash
* Card
* Other payment types

---

# Algorithmic Component

Custom algorithm implemented in:

```
scripts/dsa_ranking.py
```

Used for:

* Ranking or sorting trip data
* Demonstrating algorithm design without built-in shortcuts

---

## 🔍 Insights

# 1. The majority of trips are short-distance

Indicates high-density urban movement patterns.

# 2. Cash payments remain significant

Despite digital payment growth, cash is still widely used.

# 3. Cost efficiency varies significantly

Trips with shorter durations tend to have higher cost per mile.


# Challenges Faced

* Handling missing and inconsistent data
* Mapping numeric payment types to readable values
* Debugging frontend-backend connection issues
* Ensuring smooth data flow across the pipeline


# Future Improvements

* Add geospatial visualization (maps)
* Implement advanced filters (time, borough)
* Deploy the application online
* Improve UI/UX design


## 📸 Screenshots

### 1. Dashboard Overview

<img width="1826" height="904" alt="Screenshot 2026-06-21 152528" src="https://github.com/user-attachments/assets/f909f943-9d2d-43e7-b399-2ce883864ee7" />


# 2. Payment Chart

<img width="706" height="443" alt="Screenshot 2026-06-21 152450" src="https://github.com/user-attachments/assets/6288175b-484b-4df7-9aa5-9514b08702a3" />


# 3. API Response

<img width="1044" height="610" alt="Screenshot 2026-06-21 152431" src="https://github.com/user-attachments/assets/8e509df7-b673-4960-a64c-21042499a3cb" />


### 4. Database View

<img width="665" height="270" alt="Screenshot 2026-06-21 153449" src="https://github.com/user-attachments/assets/b998c51d-2b45-45c9-adf1-d12ad71dbc80" />



# Team Members

* Oluwatomi Thompson
* Joseph Oke
* Nyayth Chol


# License

This project was developed for academic purposes as part of the Enterprise Web Development course.


# Acknowledgements

* NYC Taxi & Limousine Commission (TLC)
* Flask Documentation
* Chart.js Documentation
* Enterprise Web Development Course
