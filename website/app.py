from flask import Flask, render_template


app = Flask(__name__)


MAPBOX_ACCESS_KEY = 'pk.eyJ1IjoidGxldWNiIiwiYSI6ImNrN2N3d3h1aTA0YWwzaHFoNGJreDJmY2YifQ.pbWSn9txb4n8fKmUaKAG4g'

lat_input = [37.87119088,37.87119088,37.87260911,37.87260911,37.87119088]
lon_input = [-122.2593983,-122.2576017,-122.2576017,-122.2593983,-122.2593983]

map_output = [[a, b] for a, b in zip(lon_input, lat_input)]


@app.route('/')
def index():
	return render_template('index.html', ACCESS_KEY = MAPBOX_ACCESS_KEY, map_output = map_output)

# @app.route('/polygon')
# def polygon_map():
# 	return 

if __name__ == '__main__':
	app.run(debug=True)
