# import all necessary libraries
import ast
import json
import csv
import mapbox
import urllib
import gmplot
import requests
import numpy as np
import geopandas as gpd
from shapely import geometry
from shapely.geometry import Point
from csv import reader
from mapbox import Geocoder
from flask import Flask, request, render_template
from math import radians, degrees, sin, cos, asin, acos, sqrt

# initialize Flask
app = Flask(__name__)

# mapbox api key
MAPBOX_ACCESS_KEY = 'pk.eyJ1IjoidGxldWNiIiwiYSI6ImNrN2N3d3h1aTA0YWwzaHFoNGJreDJmY2YifQ.pbWSn9txb4n8fKmUaKAG4g'


def great_circle(lat1, lon1, lat2, lon2):
	"""
	This function calculates the shortest distance between two sets of coordinates.
	"""

	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

	# use 6371 if calculating kilometers (3958.756 for miles)
	return 3958.756 * (acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2)))


def read_csv():
	"""
	This function reads the polygon csv file and returns the coordinates to create the polygon in mapbox
	to be displayed in the html file.
	"""

	# setting up list
	lat_input = []
	lon_input = []

	# read CSV file but skipped header line in read
	with open('static/polygon.csv', 'r') as read_line:
	    csv_reader = reader(read_line)
	    header = next(csv_reader)
	    # Check file as empty
	    if header != None:
	        # Iterate over each row after the header in the csv
	        for row in csv_reader:
	        	lat_input.append(ast.literal_eval(row[1]))
	        	lon_input.append(ast.literal_eval(row[0]))

	map_output = [[a, b] for a, b in zip(lon_input, lat_input)]

	return map_output


def convert_point(lat,lon):
    """
    Convert Coordinate Reference systems from map lat/lon to fire raster CRS
    Input: Point of latitude,longitude
    Output: Tuple of (x,y) in CRS coordinates
    """

    # Declare point
    point = Point(lat,lon)

    # Set Source CRS (Mapbox or Google Maps)
    src_crs = "EPSG:4326"

    # create dataframe from input lat/long
    gdf=gpd.GeoDataFrame(index=[0],crs = src_crs, geometry=[point])

    # Change CRS to match Wildfire CRS (3857)
    gdf_tf = gdf.to_crs("epsg:3857")

    # pull x and y value out from the POINT attribute, then get
    # the value in the data series at row[0]
    x = gdf_tf.geometry.x.at[0]
    y = gdf_tf.geometry.y.at[0]

    return (x,y)


def convert_polygon(fire_polygon):
    """Convert Coord ref system (CRS) from fire data (EPSG 3857) to map 
    lat/long (EPSG 4326), polygon starts and ends on same point (to close it)
    
    Input: list containing tuples of x,y points in fire CRS that describe a polygon
    Output: list containing tuples of lat/long points that describe the polygon
    """
    
    # create polygon
    poly = geometry.Polygon([(p[0], p[1]) for p in fire_polygon])
    
    #CRS
    src_crs = "EPSG:3857"
    dst_crs = "EPSG:4326"
    
    # Create Geo DataFrame
    gfp = gpd.GeoDataFrame(index=[0],crs=src_crs,geometry=[poly])
    
    # Convert CRS
    gfp2 = gfp.to_crs(dst_crs)
    
    # pull data from dataframe
    polyout = gfp2.iloc[0]['geometry']
    
    # create list of tuples, but longitude is first
    l = list(map(tuple,np.asarray(polyout.exterior.coords)))
    l = list(map(lambda m: (m[1],m[0]), l))
    
    return l
    

def get_lat_loc(address):
	"""
	Convert a string of address to latitude and longitude 
	Input: String 
	Output: latitude, longitude coordinate
	"""

	geocoder = mapbox.Geocoder(access_token = MAPBOX_ACCESS_KEY)
	response = geocoder.forward(address)
	address = response.json()
	add_lat = address["features"][0]["center"][1]
	add_lon = address["features"][0]["center"][0]
	return add_lat, add_lon


def active_fire(lat_origin, lon_origin):
	"""
	Function to find coordinates of active fires of given origin
	Input: latitude, longitude of input address (origin)
	Output: List of active fires within certain miles of origin
	"""

	# read JSON on active fire
	url = 'https://www.fire.ca.gov/umbraco/api/IncidentApi/List?inactive=true'
	geo_data = requests.get(url).json()

	# set variables
	lat_geo = []
	lon_geo = []
	geo_list = []

	# loop through list provided by Cal Fire and find active fire within certain miles of origin
	for i in range(0,len(geo_data)):
	    if geo_data[i]['IsActive'] == "Y":
	        fire_lat = geo_data[i]['Latitude']
	        fire_lon = geo_data[i]['Longitude']
	        dist = great_circle(lat_origin, lon_origin, fire_lat, fire_lon)
	        if dist <= 100:
	        	lat_geo.append(fire_lat)
	        	lon_geo.append(fire_lon)

	geo_list = [[a, b] for a, b in zip(lon_geo, lat_geo)]

	# geo_list = [[-122.25760168471588, 37.87119087974465]]
	return geo_list


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/fire_map', methods=["GET", "POST"])
def fire_map():

	geo_list = []
	add_loc = []

	address = "Berkeley, CA"
	if request.method == "POST":
		address = str(request.form["address"])
	
	add_lat, add_lon = get_lat_loc(address)
	
	geo_list = active_fire(add_lat, add_lon)

	for i in range(0, len(geo_list)):
		geo_lat = geo_list[i][1]
		geo_lon = geo_list[i][0]
		crs = convert_point(geo_lat, geo_lon)

	map_output = read_csv()
	return render_template('/fire_map.html', 
							ACCESS_KEY = MAPBOX_ACCESS_KEY, 
							map_output = map_output, 
							add_loc = [add_lon, add_lat],
							geo_list = geo_list)


if __name__ == '__main__':
	app.run(debug=True)
