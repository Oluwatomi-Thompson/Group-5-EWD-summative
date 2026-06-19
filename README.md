# NYC Urban Mobility Dashboard

# Overview

The **NYC Urban Mobility Dashboard** is a full-stack web application developed for the **Enterprise Web Development Summative Project**. The application provides interactive visualizations and insights into New York City taxi trip data using a responsive frontend, a Flask backend, and a SQLite database.

The project demonstrates the complete data pipeline—from raw dataset processing and storage to API development and frontend visualization.

---

# Features

* Responsive user interface
* Interactive dashboard
* Charts powered by Chart.js
* Flask REST API
* SQLite database integration
* Processed NYC Taxi dataset
* Summary statistics
* Dynamic data fetching using JavaScript Fetch API
* Mobile-friendly design

---

# Technologies Used

# Frontend

* HTML5
* CSS3
* JavaScript (ES6)
* Chart.js

# Backend

* Python
* Flask
* Flask-CORS

# Database

* SQLite

# Data Processing

* Pandas
* NumPy

---

# Project Structure

```
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
│   └── clean_data.py
│
├── .gitignore
└── README.md
```

---

## Dataset

This project uses the **NYC Yellow Taxi Trip Records** published by the New York City Taxi and Limousine Commission (TLC).

The dataset contains information including:

* Pickup locations
* Drop-off locations
* Trip distance
* Fare amount
* Passenger count
* Payment type
* Trip duration

The raw data is cleaned and processed before being stored in a SQLite database for efficient querying.

## Installation

### Clone the repository

```bash
git clone https://github.com/Oluwatomi-Thompson/Group-5-EWD-summative.git
```

Navigate into the project directory:

```bash
cd Group-5-EWD-summative
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run the Backend

```bash
cd backend
python app.py
```

The Flask server will start on:

```
http://127.0.0.1:5000
```

# Run the Frontend

Open the frontend folder using **Live Server** in Visual Studio Code or serve it with any local web server.


API Endpoints

# GET /api/summary

Returns key dashboard statistics, including:

* Total Trips
* Average Fare
* Average Distance


# GET /api/payment-types

Returns payment method distribution used to generate the pie chart.

# GET /api/monthly-trips

Returns monthly trip totals used for the line chart.

# GET /api/borough-trips

Returns trip counts grouped by borough.


#Screenshots

# Homepage


# Dashboard



# Future Improvements

* User authentication
* Real-time taxi data
* Interactive maps
* Advanced filtering
* Download reports as CSV/PDF
* Additional dashboard analytics

---

## Team Members

* Oluwatomi Thompson
* Joseph Oke
* Nyayth Chol
* Group 5 Members


# License

This project was developed for academic purposes as part of the Enterprise Web Development course.


# Acknowledgements

* New York City Taxi and Limousine Commission (TLC)
* Flask Documentation
* Chart.js Documentation
* Enterprise Web Development Course
