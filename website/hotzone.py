import ast
import json
import csv
import mapbox
import urllib
import gmplot
import requests
from csv import reader
from mapbox import Geocoder
from flask import Flask, request, render_template
from math import radians, degrees, sin, cos, asin, acos, sqrt
# from wtforms import Form

# initialize Flask
app = Flask(__name__)

# mapbox api key
MAPBOX_ACCESS_KEY = 'pk.eyJ1IjoidGxldWNiIiwiYSI6ImNrN2N3d3h1aTA0YWwzaHFoNGJreDJmY2YifQ.pbWSn9txb4n8fKmUaKAG4g'

# function to calculate distance between two sets of coordinates
def great_circle(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # use 6371 if calculating kilometers (3958.756 for miles)
    return 3958.756 * (acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2)))

# function to read csv file
def read_csv():
	'''
	This function reads the polygon csv file and returns the coordinates to create the polygon in mapbox
	to be displayed in the html file.
	'''

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

# def lat_loc():
# 	text = request.form['text']
#     address = text.upper()
# 	# address = input("Enter address (example: 2000 Carleton Street, Berkeley, CA): ")
# 	return address

# function to retrieve latitude and longitude from address entry
def get_lat_loc(address):
	geocoder = mapbox.Geocoder(access_token = MAPBOX_ACCESS_KEY)
	response = geocoder.forward(address)
	address = response.json()
	add_lat = address["features"][0]["center"][1]
	add_lon = address["features"][0]["center"][0]
	return add_lat, add_lon

# function to find coordinates of active fires of given orgin
def active_fire(lat_orgin, lon_orgin):

	# read JSON on active fire
	url = 'https://www.fire.ca.gov/umbraco/api/IncidentApi/List?inactive=true'
	geo_data = requests.get(url).json()

	# set 
	lat_geo = []
	lon_geo = []
	geo_list = []

	for i in range(0,len(geo_data)):
	    if geo_data[i]['IsActive'] == "Y":
	        fire_lat = geo_data[i]['Latitude']
	        fire_lon = geo_data[i]['Longitude']
	        dist = great_circle(lat_orgin, lon_orgin, fire_lat, fire_lon)
	        if dist <= 100:
	        	lat_geo.append(fire_lat)
	        	lon_geo.append(fire_lon)

	# geo_list = [[a, b] for a, b in zip(lon_geo, lat_geo)]

	geo_list = [[-122.25760168471588, 37.87119087974465],[-122.25760168471588, 37.87260911343006]]
	return geo_list

@app.route('/')
def index():
	return render_template('index.html')

# class ReusableForm(Form):
#     name = TextField('Address:')
    
#     @app.route("/fire_map", methods=['GET', 'POST'])
#     def hello():
#         form = ReusableForm(request.form)
    
#         print (form.errors)
#         if request.method == 'POST':
#             name=request.form['name']
#             print (name)
    
#         # if form.validate():
#         #     # Save the comment here.
#         #     flash('Hello ' + name)
#         # else:
#         #     flash('All the form fields are required. ')
#         return render_template('hello.html', form=form)

@app.route('/fire_map', methods=["GET", "POST"])
def fire_map():
	geo_list = []
	add_loc = []
	# errors = ""
	address = "2535 Channing Way, Berkeley, CA"
	if request.method == "POST":
		address = str(request.form["address"])
	add_lat, add_lon = get_lat_loc(address)
	geo_list = active_fire(add_lat, add_lon)
	map_output = read_csv()
	return render_template('/fire_map.html', 
							ACCESS_KEY = MAPBOX_ACCESS_KEY, 
							map_output = map_output, 
							add_loc = [add_lon, add_lat],
							geo_list = geo_list)

# @app.route('/fire_map', methods=["GET", "POST"])
# def fire_map_post():
	# errors = ""
	# if request.method == "POST":
	# 	address = None
	# 	address = str(request.form["address"])
# 		return 

if __name__ == '__main__':
	app.run(debug=True)
