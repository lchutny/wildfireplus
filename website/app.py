import ast
import csv
from csv import reader
from flask import Flask, render_template

# initialize Flask
app = Flask(__name__)

# mapbox api
MAPBOX_ACCESS_KEY = 'pk.eyJ1IjoidGxldWNiIiwiYSI6ImNrN2N3d3h1aTA0YWwzaHFoNGJreDJmY2YifQ.pbWSn9txb4n8fKmUaKAG4g'

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

@app.route('/')
def index():
	return render_template('index.html', ACCESS_KEY = MAPBOX_ACCESS_KEY, map_output = map_output)

if __name__ == '__main__':
	app.run(debug=True)
