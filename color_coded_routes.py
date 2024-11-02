import googlemaps
import folium
import pandas as pd
from streamlit_folium import st_folium
import streamlit as st

# Replace with your Google Maps API key
API_KEY = 'YOUR_API_KEY'
gmaps = googlemaps.Client(key=API_KEY)

# Starting and destination locations (latitude, longitude)
start_location = (37.7749, -122.4194)  # Example: San Francisco
end_location = (37.3382, -121.8863)    # Example: San Jose

# Request directions data from Google Maps API
directions = gmaps.directions(
    origin=start_location,
    destination=end_location,
    mode="walking",
    departure_time="now"
)

# Define color codes for sidewalk conditions
condition_colors = {
    "Good": "green",
    "Moderate": "yellow",
    "Poor": "orange",
    "Severely Damaged": "red"
}

# Simulate condition data for each route segment
# (In practice, this could come from a dataset or API response)
# Here, we assign random conditions for illustration.
import random
conditions = ["Good", "Moderate", "Poor", "Severely Damaged"]

# Parse the directions and extract each step in the route
route_data = []
for step in directions[0]['legs'][0]['steps']:
    # Extract latitude and longitude from the start and end of each step
    start_lat = step['start_location']['lat']
    start_lng = step['start_location']['lng']
    end_lat = step['end_location']['lat']
    end_lng = step['end_location']['lng']
    
    # Assign a random condition to each segment (replace with real data in practice)
    condition = random.choice(conditions)
    color = condition_colors[condition]  # Map condition to color
    
    route_data.append({
        "start": (start_lat, start_lng),
        "end": (end_lat, end_lng),
        "condition": condition,
        "color": color
    })

# Initialize the map centered at the start location
m = folium.Map(location=start_location, zoom_start=12)

# Add each step as a colored line to the map
for segment in route_data:
    folium.PolyLine(
        locations=[segment['start'], segment['end']],
        color=segment['color'],
        weight=5,
        opacity=0.7,
        tooltip=f"Condition: {segment['condition']}"
    ).add_to(m)

# Display the map in Streamlit
st.title("Color-Coded Accessibility Route Map")
st_folium(m, width=700, height=500)
