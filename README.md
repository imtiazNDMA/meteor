# M.E.T.E.O.R 
**Meteorological Environment Tracking, Extraction, and Observation Resource**

A modern Python GUI application for accessing and analyzing meteorological data from various sources. Built with Tkinter and powered by Meteostat APIs.

## Features

- 🌍 **Geocoding Integration**: Convert location names to coordinates using OpenStreetMap
- 📅 **Flexible Time Frames**: Choose from multiple data frequencies:
  - Hourly
  - Daily
  - Monthly
  - Climate Normals (30-year averages)
- 📊 **Data Visualization**:
  - Interactive line charts for temperature, precipitation, and wind speed
  - Multi-variable comparison views
  - Data preview tables
- ⏲ **Real-time Clock**: Always visible time display
- 📤 **Export Capabilities**: Save data as CSV or Excel files
- 🗺 **Coordinate Input**: Direct latitude/longitude entry or location search

## Installation

1. **Prerequisites**:
   - Python 3.6+
   - pip package manager

2. **Install dependencies**:
```bash
pip install meteostat geopy pandas matplotlib tkcalendar
