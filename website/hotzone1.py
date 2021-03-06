# import all necessary libraries / packages
import ast
import json
import csv
import mapbox
import urllib
import requests
import re
import boto3
import datetime
import io
import os
import pickle
import itertools
import keras
import tensorflow
import numpy as np
import pandas as pd
import rasterio as rio
import geopandas as gpd
from shapely import geometry
from shapely.geometry import Polygon
from shapely.geometry import Point
from csv import reader
from mapbox import Geocoder
from flask import Flask, request, render_template
from math import radians, degrees, sin, cos, asin, acos, sqrt


# initialize Flask
app = Flask(__name__)

# mapbox api key
MAPBOX_ACCESS_KEY = 'pk.eyJ1IjoidGxldWNiIiwiYSI6ImNrN2N3d3h1aTA0YWwzaHFoNGJreDJmY2YifQ.pbWSn9txb4n8fKmUaKAG4g'

class DataStore():
    a = None
    coords = [[-121.91030200875473, 36.49549958363892],[-121.89706675496642, 36.49549958363892],[-121.91471376001749, 36.49132363869813],[-121.89265500370365, 36.49132363869813],[-121.91912551128027, 36.48714769375733],[-121.89706675496642, 36.48714769375733],[-121.92353726254304, 36.48297174881653],[-121.89706675496642, 36.48297174881653],[-121.93236076506857, 36.478795803875734],[-121.88824325244089, 36.478795803875734],[-121.93677251633135, 36.474619858934936],[-121.88824325244089, 36.474619858934936],[-121.9279490138058, 36.47044391399414],[-121.88383150117812, 36.47044391399414],[-121.92353726254304, 36.46626796905334],[-121.91471376001749, 36.46626796905334],[-121.90589025749196, 36.46626796905334],[-121.87941974991534, 36.46626796905334],[-121.9279490138058, 36.46209202411254],[-121.87941974991534, 36.46209202411254],[-121.92353726254304, 36.457916079171746],[-121.86618449612705, 36.457916079171746],[-121.8441257398132, 36.457916079171746],[-121.83971398855043, 36.457916079171746],[-121.92353726254304, 36.45374013423095],[-121.8573609936015, 36.45374013423095],[-121.92353726254304, 36.44956418929015],[-121.85294924233874, 36.44956418929015],[-121.91912551128027, 36.44538824434935],[-121.84853749107596, 36.44538824434935],[-121.9279490138058, 36.441212299408555],[-121.90589025749196, 36.441212299408555],[-121.89265500370365, 36.441212299408555],[-121.87941974991534, 36.441212299408555],[-121.87500799865258, 36.441212299408555],[-121.84853749107596, 36.441212299408555],[-121.83971398855043, 36.441212299408555],[-121.82647873476212, 36.441212299408555],[-121.9279490138058, 36.43703635446776],[-121.90589025749196, 36.43703635446776],[-121.89265500370365, 36.43703635446776],[-121.87059624738981, 36.43703635446776],[-121.86618449612705, 36.43703635446776],[-121.81765523223659, 36.43703635446776],[-121.91471376001749, 36.43286040952696],[-121.89706675496642, 36.43286040952696],[-121.89265500370365, 36.43286040952696],[-121.87500799865258, 36.43286040952696],[-121.86177274486427, 36.43286040952696],[-121.81324348097381, 36.43286040952696],[-121.90589025749196, 36.42868446458617],[-121.89706675496642, 36.42868446458617],[-121.89265500370365, 36.42868446458617],[-121.87059624738981, 36.42868446458617],[-121.85294924233874, 36.42868446458617],[-121.82647873476212, 36.42868446458617],[-121.91030200875473, 36.42450851964537],[-121.87500799865258, 36.42450851964537],[-121.84853749107596, 36.42450851964537],[-121.82647873476212, 36.42450851964537],[-121.90589025749196, 36.420332574704574],[-121.86618449612705, 36.420332574704574],[-121.83971398855043, 36.420332574704574],[-121.82206698349935, 36.420332574704574],[-121.89706675496642, 36.416156629763776],[-121.86177274486427, 36.416156629763776],[-121.83971398855043, 36.416156629763776],[-121.81324348097381, 36.416156629763776],[-121.89265500370365, 36.41198068482298],[-121.87941974991534, 36.41198068482298],[-121.87500799865258, 36.41198068482298],[-121.80883172971104, 36.41198068482298],[-121.89706675496642, 36.40780473988218],[-121.87941974991534, 36.40780473988218],[-121.87500799865258, 36.40780473988218],[-121.80883172971104, 36.40780473988218],[-121.88383150117812, 36.40362879494138],[-121.80000822718551, 36.40362879494138],[-121.88383150117812, 36.399452850000586],[-121.82206698349935, 36.399452850000586],[-121.87941974991534, 36.39527690505979],[-121.82206698349935, 36.39527690505979],[-121.81765523223659, 36.39527690505979],[-121.80441997844828, 36.39527690505979],[-121.87500799865258, 36.39110096011899],[-121.80883172971104, 36.39110096011899],[-121.86177274486427, 36.38692501517819],[-121.80441997844828, 36.38692501517819],[-121.8573609936015, 36.382749070237395],[-121.85294924233874, 36.382749070237395],[-121.8441257398132, 36.382749070237395],[-121.83530223728766, 36.382749070237395],[-121.83971398855043, 36.3785731252966],[-121.82647873476212, 36.3785731252966],[-121.86618449612705, 36.361869345533414],[-121.86177274486427, 36.361869345533414],[-121.80441997844828, 36.361869345533414],[-121.80000822718551, 36.361869345533414],[-121.79559647592274, 36.361869345533414],[-121.79118472465997, 36.361869345533414],[-121.82206698349935, 36.357693400592616],[-121.81765523223659, 36.357693400592616],[-121.8573609936015, 36.34516556577022],[-121.85294924233874, 36.34516556577022]]


data = DataStore()
glalat = None
glalon = None
glday0 = None
glday1 = None
glday2 = None
glfirename = None

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


def write_csv(poly, filename):
	"""
	This function writes the active fire intial polygon to csv to be used for the ML model to calculate
	spread on the next day.
	"""
	# f = open("/static/intial_polygon.csv", "w")
	# f.truncate()
	# f.close()
	filename = filename

	with open(filename, "w") as f:
		writer = csv.writer(f)
		writer.writerows(poly)


def convert_point(lat,lon):
    """
    Convert Coordinate Reference systems from map lat/lon to fire raster CRS
    Input: Point of latitude,longitude
    Output: Tuple of (x,y) in CRS coordinates
    """

    # Declare point (longitude (or x) always comes first, then latitude (y))
    point = Point(lon,lat)

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


def get_loc(address):
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


def chk_polygon(pt_lon, pt_lat):
	"""
	This function checks to see if address entered is within the polygon of data the model is trained on
	Input: string
	Output: boolean
	"""

	# the coordinates of the polygon
	coords = [(-123.5,39), (-119.5,39), (-119.5,36), (-123.5,36),(-123.5,39)]
	poly_bound = Polygon(coords)

	# check ot see if provided coordinate is within the boundary of the polygon
	point_interest = Point(pt_lon, pt_lat)
	result = point_interest.within(poly_bound)

	return result


def points(poly):
    return list(map(tuple,np.asarray(poly.exterior.coords)))


def active_fire():
	"""
	Function to find coordinates of all current active fires from url
	Input: N/A
	Output: List of tuples of active fires
	"""

	# set variables
	lat_geo = []
	lon_geo = []
	geo_fire = []

	# list of the States in USA
	states = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','South Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']

	# read JSON on active fire
	url = 'https://opendata.arcgis.com/datasets/5da472c6d27b4b67970acc7b5044c862_0.geojson'
	# geo_data = requests.get(url).json()
	geo_data = gpd.read_file(url)

	poly_list = geo_data.geometry

	# grab the first coordinates of all polygons to create list of active fires

	for m in range(0,len(poly_list)):

		if poly_list[m].geom_type == 'MultiPolygon':

			geo_poly = points(poly_list[m][0])

			fire_lon = geo_poly[0][0]
			fire_lat = geo_poly[0][1]

			lat_geo.append(fire_lat)
			lon_geo.append(fire_lon)

		else:

			geo_poly = points(poly_list[m])

			fire_lon = geo_poly[0][0]
			fire_lat = geo_poly[0][1]

			lat_geo.append(fire_lat)
			lon_geo.append(fire_lon)

	geo_fire = [[a, b] for a, b in zip(lon_geo, lat_geo)]

	#
	fire_names = geo_data.IncidentName
	acres = geo_data.GISAcres

	geocoder = mapbox.Geocoder(access_token = MAPBOX_ACCESS_KEY)

	loc_output = []
	state_output = []

	for l in range(0,len(geo_fire)):

		rev_lon = geo_fire[l][0]
		rev_lat = geo_fire[l][1]

		response = geocoder.reverse(lon=rev_lon, lat=rev_lat)

		features = response.geojson()['features']

		loc_name = features[0]["place_name"]

		loc_output.append(loc_name)

		result = loc_name.split(",")

		for s in range(0,len(result)):
			res = result[s]
			res1 = re.sub(r'[0-9]+', '',res)
			res2 = res1.strip()
			if res2 in states:
				state_output.append(res2)
				break

	firename = []

	for f in range(0,len(fire_names)):
		firename.append(fire_names[f])

	fireacre = []

	for a in range(0,len(acres)):
		fireacre.append(acres[a])

	firestate = pd.Series(state_output)

	fireloc = pd.Series(loc_output)

	firename = pd.Series(firename)

	fireacre = pd.Series(fireacre)

	df = {"State": firestate, "Active Fire Name": firename, "Approximate Fire Location": fireloc, "Acres Burned": fireacre }

	fire_table = pd.DataFrame(df)

	fire_table = fire_table.sort_values(by=["State"])

	fire_table = fire_table.reset_index(drop=True)

	fire_table.index = fire_table.index + 1

	return geo_fire, fire_table, geo_data


def chk_fire(lon_origin, lat_origin, geo_data):
    """Function to find coordinates of active fires of given origin
    Input: latitude, longitude of input address (origin)
    Output: List of active fires within certain miles of origin
    """

    # set variables
    geo_center = []
    poly_list = geo_data.geometry
    geo_poly = []
    fire_num = None

    for i in range(0,len(poly_list)):
        if len(geo_center) > 0:
            break

        if poly_list[i].geom_type == 'MultiPolygon':

            for j in range(0, len(poly_list[i])):
                geo_poly = points(poly_list[i][j])

                for k in range(0, len(geo_poly)):
                    fire_lon = geo_poly[k][0]
                    fire_lat = geo_poly[k][1]

                    dist = great_circle(lat_origin, lon_origin, fire_lat, fire_lon)
                    if dist <= 100:
                        geo_center = [fire_lon, fire_lat]
                        fire_num=i
                        break
                if len(geo_center) > 0:
                    break
            if len(geo_center) > 0:
                break

        else:
            geo_poly = points(poly_list[i])

            for j in range(0, len(geo_poly)):
                fire_lon = geo_poly[j][0]
                fire_lat = geo_poly[j][1]

                dist = great_circle(lat_origin, lon_origin, fire_lat, fire_lon)
                if dist <= 100:
                    geo_center = [fire_lon, fire_lat]
                    fire_num=i
                    break

            if len(geo_center) > 0:
                break

        if len(geo_center) > 0:
            break
        else:
            geo_poly =[]
            break
    # convert to format for prediction
    geo_poly = [tuple(l) for l in geo_poly]

    return geo_center, geo_poly, fire_num

# codes for CNN prediction

# s3 config
s3_client = boto3.client('s3')
bucket_name = 'hotzone'


def pull_data_from_s3(s3_client, bucket_name, key_name):
    '''
    Pulls pre-processed data from S3.

    Args:
        - s3_client: boto3 s3 client
        - bucket_name: name of bucket on s3 to pull data from
        - key_name: directory/file_name to pull data from
    Returns:
        - Nothing

    https://stackoverflow.com/questions/48049557/how-to-write-npy-file-to-s3-directly
    '''

    array_data = io.BytesIO()
    s3_client.download_fileobj(bucket_name, key_name, array_data)

    array_data.seek(0)
    array = pickle.load(array_data)

    return array


def get_index(long,lat):

    '''
    Get the pixel of a given coordinate.

    Args:
        - Long: longitude of point
        - Lat: latitude of point
    Returns:
        - pixelrow: index of row of point
        - pixelcol: index of column of point

    '''

    left = -123.50294421461426
    top = 39.00106654811723

    xres = 0.004411751262768785
    yres = -0.0041759449407971815

    pixelcol = int(np.rint((long - left)/xres))
    pixelrow = int(np.rint((lat - top)/yres))

    return (pixelrow, pixelcol)


def get_coords(y, x):

    '''
    Get the coordinates of a given pixel in the tif coordinate system.

    Args:
        - Y: index of row of point
        - X: index of column of point
    Returns:
        - Long: longitude of point
        - Lat: latitude of point
    '''

    left = -123.50294421461426
    top = 39.00106654811723

    xres = 0.004411751262768785
    yres = -0.0041759449407971815

    deltax = xres*x
    deltay = yres*y

    long = left+deltax
    lat = top+deltay

    return (long, lat)


def get_weather(max_values, lat, long, day):

    '''
    Get tomorrow's weather forecast for fire prediction.

    Args:
        - Max_values: list of weather max_values used to scale weather
        - Lat: latitude of point to fetch weather for
        - Long: longitude of point to fetch weather for
    Returns:
        - weather: a list of weather data to use for prediction
    '''


    s = requests.Session()
    s.auth = ('user', 'pass')
    s.headers.update({'Accept-Encoding':'gzip'})
    headers = {'Accept-Encoding':'gzip'}

    key = '5ffac5f056d341c6296cba58fa96e9ba'
    date = str(datetime.date.today() + datetime.timedelta(days = day)) + 'T12:00:00'
    lat = str(lat,)
    long = str(long)
    blocks = '[currently,minutely,hourly,alerts]'
    units = 'ca'

    # set the query string for darksky
    query = ('https://api.darksky.net/forecast/'+key+'/'+
    lat+','+long+','+date+'?exclude='
    +blocks+'&units='+units)

    # Make the call to Dark Sky to get all the data for that date and location
    r = s.get(query,headers=headers)

    data = r.json()
    data = data['daily']['data'][0]

    rainint = data['precipIntensityMax']
    high_t = data['temperatureHigh']
    low_t= data['temperatureLow']
    humidity = data['humidity']
    wind_speed = data['windSpeed']
    wind_direction = data['windBearing']

    weather_data = {
        'rainint': rainint,
        'High T': high_t,
        'Low T': low_t,
        'Humidity': humidity,
        'Wind Speed': wind_speed,
        'Wind Direction': wind_direction
    }

    weather = []

    for k, v in weather_data.items():
        max_val = max_values.get(k, 1)

        if k in ['High T', 'Low T']:
            v += 273.15
        else:
            v

        val = v/float(max_val)
        weather.append(val)

    return weather


def pull_weather_maxes_from_s3():
    '''
    Pull files from S3 for the provided year and save to local directory
    '''

    s3 = boto3.resource('s3')

    key = "BayAreaWeather/max_values/max_values.pickle"
    directory = 'static/'
    path = directory + 'max_values.pickle'

    s3.Bucket('hotzone').download_file(key, path)

    total_path = os.path.abspath(directory)

    for f in os.listdir(total_path):
        if f.endswith('.pickle'):
            max_values = total_path + '/' + f

    max_values = pd.read_pickle(max_values)

    return max_values


def predict_day(lat_long_coords, day=1,threshold=0.999):

    '''
    Predict where fire will be in the next day.

    Args:
        - lat_long_coords: a list of lat/long coordinates that make up a polygon representing where fire is
    Returns:
        - prediction: a list of lat/long coordinates that make up a polygon representing where fire will be
    '''

    # load model from s3

    new_config = pull_data_from_s3(s3_client, bucket_name, 'models/model_config.pickle')
    new_weights = pull_data_from_s3(s3_client, bucket_name, 'models/model_weights.pickle')

    # Need this line to run on Laura's Machine
    keras.backend.tensorflow_backend._SYMBOLIC_SCOPE.value=True
    #  Comment out for server

    model = keras.Model.from_config(new_config)
    model.set_weights(new_weights)

    today = np.zeros((719, 908))
    side = 16

    for (long, lat) in lat_long_coords:
        index = get_index(long,lat)
        today[index] = 1

    np.pad(today, pad_width=32, mode='constant', constant_values=0)

    fire_vals = np.where(today == 1)

    x_avg = int(np.mean(fire_vals[0]))
    y_avg = int(np.mean(fire_vals[1]))

    # minimize computations by only making predictions for pixels in 50x50 square around pixel of interest
    x_min = x_avg - 50
    x_max = x_avg + 50

    x_min = max(x_min, 0)
    x_max = min(x_max, 972)

    y_min = y_avg - 50
    y_max = y_avg + 50

    y_min = max(y_min, 0)
    y_max = min(y_max, 783)


    x_vals = range(x_min, x_max)
    y_vals = range(y_min, y_max)

    vals = list(itertools.product(x_vals, y_vals))

    values = []

    shape = today.shape
    prediction = np.zeros(shape)

    (long, lat) = get_coords(x_avg, y_avg)

    # get max weather values
    max_values = pull_weather_maxes_from_s3()

    weather = get_weather(max_values, lat, long, day)

    for (xi, yi) in vals:

        point = (xi, yi)

        xi_r = int(xi + side)
        xi_l = int(xi - side)
        yi_b = int(yi + side)
        yi_t = int(yi - side)

        if xi_r > 0 and xi_l > 0 and yi_b > 0 and yi_t > 0:

            m = today[xi_l:xi_r, yi_t:yi_b]

            if (m.shape == (32, 32)):
                fire = []
                w = []

                fire.append(np.asarray(m))
                w.append(np.asarray(weather))

                fire = np.asarray(fire)
                w = np.asarray(w)

                obs = len(fire)
                fire = fire.reshape(obs, 32, 32, 1)

                val = model.predict([fire, w])

                prediction[point] = val

    # create outline of prediction
    prediction = np.where(prediction < threshold, 0, 1)

    outline = np.rint(prediction)
    outline = np.diff(outline, prepend=0)  #, prepend = 0
    outline = np.abs(outline)

    # get pixels from outline
    poly_to_plot = np.where(outline != 0)


    # instantiate a matrix in the target shape
    shape = outline.shape
    poly = np.zeros(shape)

    # create a list of coordinates in the tif coordinate system
    tif_coordinates = []

    for (xi, yi) in list(zip(poly_to_plot[0], poly_to_plot[1])):
        poly[xi,yi] = 1
        coords = get_coords(xi, yi)
        tif_coordinates.append(coords)

    return tif_coordinates

def polyplot(geo_poly):
    """Reorder the polygon points to plot in clockwise fashion
    Input: geo_poly list of (long,lat) tuples describing fire outline
    Output: geo_poly list of ordered (long,lat)tuples for plotting fire outline
    """
    # Because we always write the points along given latitude lines, we'll create
    # a left and right pair and reorder that way. For any given latitude, get left and
    # right most longitude

    geo_poly.sort(key=lambda x:x[1])
    lhs=[]
    rhs=[]

    i=0
    x=len(geo_poly)
    while i < len(geo_poly):
        lat = geo_poly[i][1]
        longs=[]
        while geo_poly[i][1] == lat:
            longs.append(geo_poly[i][0])
            i+=1
            if i==x:
                break
        lhs.append([min(longs),lat])
        rhs.append([max(longs),lat])

    # reverse lhs so that the polygon is clockwise
    lhs.reverse()
    # Stitch them back together
    geo_poly2 = rhs
    geo_poly2.extend(lhs)

    return geo_poly2

# For Flask application

@app.route('/')
def index():
	return render_template('index_R1.html')


@app.route('/fire_map', methods=["GET", "POST"])
def fire_map():

    geo_center = []
    add_loc = []
    map_output = []
    geo_fire = []
    outside_bound = "false"
    no_fire	= "false"

    global glalat,glalong,glday0,glday1,glday2,glfirename
	# call function (active_fire) to get this list of active fire for map plotting and convert it into dataframe for table visualization
    geo_fire, fire_table, geo_data = active_fire()

    address = data.a

    # POST address entered by user
    if request.method == "POST":
        address = str(request.form["address"])
        # call function (get_loc) to convert address into longitude and latitude
        add_lat, add_lon = get_loc(address)
        # check to see if address entered is within the polygon the model is trained on
        if chk_polygon(add_lon, add_lat):
            outside_bound = "false"
        else:
            outside_bound = "true"
    else:
       # set initial address to Berkeley
       address = "Berkeley, CA"
       # call function (get_loc) to convert address into longitude and latitude
       add_lat, add_lon = get_loc(address)

    # Set address to global variable
    data.a = address
    glalat = add_lat
    glalon = add_lon

	# call chk_fire function with the address coordinates and find if there is an active fire nearby address of interest
    geo_center, geo_poly, fire_num = chk_fire(add_lon, add_lat,geo_data)

	# check to see if function above returns any active fire, if exist, convert the polygon to crs coordinate for model to use
    if len(geo_center) > 0:
        no_fire = "false"
        fire_name = geo_data.iloc[fire_num]['IncidentName']
        fire_acres = geo_data.iloc[fire_num]['GISAcres']
    else:
        no_fire = "true"
        fire_name = 'Example'
        fire_acres = '20,703' # From area calculation in Jupyter

    glfirename = fire_name

    return render_template('/fire_map_R1.html',
                            address_entered = address,
                            fire_name = fire_name,
                            fire_acres = fire_acres,
                            fire_table = [fire_table.to_html (classes = "ftable")],
                            ACCESS_KEY = MAPBOX_ACCESS_KEY,
                            add_loc = [add_lon, add_lat],
                            geo_fire = geo_fire,
                            no_fire = no_fire,
                            outside_bound = outside_bound)


@app.route('/fire_map1', methods=["GET", "POST"])
def fire_map1():

    geo_center = []
    add_loc = []
    map_output = []
    geo_fire = []
    map_output_day1 = []
    map_output_day2 = []
    outside_bound = "false"
    no_fire = "false"
    global glalat,glalong,glday0,glday1,glday2,glfirename

    address = data.a

    # call function (active_fire) to get this list of active fire for map plotting and convert it into dataframe for table visualization
    geo_fire, fire_table, geo_data = active_fire()
    add_lat, add_lon = get_loc(address)

    # # this calls the CNN model to predict the polygon shape for mapping for day 1 of fire
    # predict_day1 = predict_day(data.coords, 1,0.99)
    # glday1 = predict_day1
    # map_output_day1 = polyplot(predict_day1) # to convert to format for mapbox

    if glday1 == None:
        predict_day1 = predict_day(data.coords, 1,0.99)
        glday1 = predict_day1
    else:
        predict_day1 = glday1

    map_output_day1 = polyplot(predict_day1) # to convert to format for mapbox

    fire_name = glfirename

    return render_template('/fire_map1_RX.html',
                            fire_table = [fire_table.to_html (classes = "ftable")],
                            ACCESS_KEY = MAPBOX_ACCESS_KEY,
                            address_entered = address,
                            fire_name = fire_name,
                            map_output_day1 = map_output_day1,
                            add_loc = [add_lon, add_lat],
                            no_fire = no_fire,
                            outside_bound = outside_bound,
                            geo_fire = geo_fire)


@app.route('/fire_map2', methods=["GET", "POST"])
def fire_map2():

    geo_center = []
    add_loc = []
    map_output = []
    geo_fire = []
    map_output_day1 = []
    map_output_day2 = []
    outside_bound = "false"
    no_fire = "false"
    global glalat,glalong,glday0,glday1,glday2,glfirename

    # call function (active_fire) to get this list of active fire for map plotting and convert it into dataframe for table visualization
    address = data.a
    day1 = glday1

    geo_fire, fire_table, geo_data = active_fire()
    add_lat, add_lon = get_loc(address)

    # # this calls the CNN model to predict the polygon shape for mapping for day 2 of fire
    # predict_day2 = predict_day(day1, 2,0.99)
    # glday2 = predict_day2
    # map_output_day2 = polyplot(predict_day2)

    if glday2 == None:
        predict_day2 = predict_day(day1, 2,0.99)
        glday2 = predict_day2
    else:
        predict_day2 = glday2

    map_output_day2 = polyplot(predict_day2)
    map_output_day1 = polyplot(day1)

    fire_name = glfirename

    return render_template('/fire_map2_RX.html',
                            fire_table = [fire_table.to_html (classes = "ftable")],
                            address_entered = address,
                            ACCESS_KEY = MAPBOX_ACCESS_KEY,
                            fire_name = fire_name,
                            map_output_day2 = map_output_day2,
                            map_output_day1 = map_output_day1,
                            add_loc = [add_lon, add_lat],
                            no_fire = no_fire,
                            outside_bound = outside_bound,
                            geo_fire = geo_fire)

if __name__ == '__main__':
	app.run(debug=True)
