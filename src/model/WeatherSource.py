#http://www.7timer.info/bin/api.pl?lon=113.17&lat=23.09&product=astro&output=xml
import requests
import json
import subprocess
import sys
#from Entry import *i
"""try:
    import geopy
    print("geopy is already installed")
except ImportError:
    print("geopy not found. Using pip to install")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "geopy"])
    print("geopy installed successfully!")"""
#import pandas as pd

# Data for each state with its latitude and longitude
data = {
    "State": [
        "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", 
        "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", 
        "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", 
        "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", 
        "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", 
        "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", 
        "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", 
        "Wisconsin", "Wyoming"
    ],
    "City": [
        ("Montgomery","Birmingham"), ("Anchorage","Fairbanks"), ("Phoenix","Tucson"), ("Little Rock","Fayetteville"), "Sacramento", "Denver", "Hartford",
        "Dover", "Tallahassee", "Atlanta", "Honolulu", "Boise", "Springfield", "Indianapolis", "Des Moines",
        "Topeka", "Frankfort", "Baton Rouge", "Augusta", "Annapolis", "Boston", "Lansing",
        "Saint Paul", "Jackson", "Jefferson City", "Helena", "Lincoln", "Carson City", "Concord",
        "Trenton", "Santa Fe", "Albany", "Raleigh", "Bismarck", "Columbus",
        "Oklahoma City", "Salem", "Harrisburg", "Providence", "Columbia", "Pierre",
        "Nashville", "Austin", "Salt Lake City", "Montpelier", "Richmond", "Olympia",
        "Charleston", "Madison", "Cheyenne"
    ],
    "Latitude": [
        32.8067, 61.3707, 33.7298, 34.9697, 36.1162, 39.0598, 41.5978, 
        39.3185, 27.7663, 33.0406, 21.0943, 44.2405, 40.3495, 39.8494, 42.0115, 
        38.5266, 37.6681, 31.1695, 44.6939, 39.0639, 42.2302, 43.3266, 
        45.6945, 32.7416, 38.4561, 46.9219, 41.1254, 38.3135, 43.4525, 
        40.2989, 34.8405, 42.1657, 35.6301, 47.5289, 40.3888, 
        35.5653, 44.5720, 40.5908, 41.6809, 33.8569, 44.2998, 
        35.7478, 31.0545, 40.1500, 44.0459, 37.7693, 47.4009, 
        38.4912, 44.2685, 42.7560
    ],
    "Longitude": [
        -86.7911, -152.4044, -111.4312, -92.3731, -119.6816, -105.3111, -72.7554, 
        -75.5071, -81.6868, -83.6431, -157.4983, -114.4788, -88.9861, -86.2583, -93.2105, 
        -96.7265, -84.6701, -91.8678, -69.3819, -76.8021, -71.5301, -84.5361, 
        -93.9002, -89.6787, -92.2884, -110.4544, -98.2681, -117.0554, -71.5639, 
        -74.5210, -106.2485, -74.9481, -79.8064, -99.7840, -82.7649, 
        -96.9289, -122.0709, -77.2098, -71.5118, -80.9450, -99.4388, 
        -86.6923, -97.5635, -111.8624, -72.7107, -78.1700, -121.4905, 
        -80.9545, -89.6165, -107.3025
    ]
}

# Create a DataFrame
userChoice = "Phoenix"
stateNum = 0
cityNum = 0
long = 0.0
lat = 0.0

for i in range(len(data["State"])):
    if data["State"][i] == userChoice:
        stateNum = i

for k in range(len(data["City"])):
    if userChoice in data["City"][k]:
        cityNum = k

for j in range(len(data["Longitude"])):
    if j in (stateNum,cityNum):
        long = data["Longitude"][j]
        lat = data["Latitude"][j]



print("The num: ",stateNum)
# Save as a CSV file
#from geopy.geocoders import Nominatim

#def get_lat_long(state_name):
#    geolocator = Nominatim(user_agent="geoapiExercises")
#    location = geolocator.geocode(state_name)
#    
#    if location:
#        return (location.latitude, location.longitude)
#    else:
#        return None

query = "Arizona"
#latLong = get_lat_long(query)
#print(latLong)    
response = requests.get("https://api.open-meteo.com/v1/forecast?latitude="+str(lat)+"&longitude="+str(long)+"&current=temperature_2m,wind_speed_10m,apparent_temperature")

if response.status_code == 200:
    print(response.json())
