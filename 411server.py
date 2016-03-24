from flask import Flask, request, jsonify, abort
app = Flask(__name__)
import googlemaps
import json
from urllib2 import urlopen
from datetime import datetime
import numpy as np

now = datetime.now()
# from geolocation.google_maps import GoogleMaps
# from geolocation.distance_matrix import const




gmaps = googlemaps.Client(key='AIzaSyDyIjazEKwGObz96R856yDFMuNJJXXPzyU')


spaces = ["37 Buswell street, Boston","22 cummington mall, Boston","232 bay state road, Boston","975 Gaffney road, Boston","2 bay state Road, Boston"]

def setLocation(loc):
	geoSpaces = [] 
	for i in range(len(spaces)):
		distance = gmaps.distance_matrix(loc, spaces[i])
		km = distance['rows'][0]['elements'][0]['distance']['text']
		km = km[:-3]
		km = float(km)
		if km < 1:
			geoSpaces.append(spaces[i])
	closeSpaces = []
	print geoSpaces
	for j in range(len(geoSpaces)):
		geocode_result = gmaps.geocode(geoSpaces[j])
		#print geocode_result
		lat = geocode_result[0]['geometry']['location']['lat']
		lng = geocode_result[0]['geometry']['location']['lng']
		closeSpaces.append(np.asarray([lat,lng, geoSpaces[j]]))
	print closeSpaces

setLocation("200 Bay State Road, Boston")




#Server Stuff

# '''
# Backend for TODOs
# '''

# todos = [{'id':0, 'item':'sample_todo'}]

# def add_item(item):
# 	global todos
# 	if 'id' in item and 'item' in item:
# 		todos.append(item)
# 	else:
# 		print('invalid format')

# def remove_item(id):
# 	global todos
# 	todos = [todo for todo in todos if not todo['id'] == id]




# @app.route('/')
# def index():
# 	return 'hello world'

# @app.route('/post', methods = ['POST'])
# def post():
# 	global x
# 	if not request.json: 
# 		abort(500)
# 	if 'x' in request.json:
# 		x = request.json['x']
# 		return jsonify({'x':x}), 200
# 	else:
# 		return jsonify({'error':'invalid format'}), 500

# @app.route('/get', methods = ['GET'])
# def get():
# 	return jsonify({'x':x}), 200

# @app.route('/add', methods = ['POST'])
# def add():
# 	# TODO Add you code here.
# 	if not request.json: 
# 		abort(500)
# 	if 'id' in request.json:
# 		add_item({"id":request.json["id"],"item":request.json["item"]})
# 		return jsonify({'todo_list':todos}), 200
# 	else:
# 		return jsonify({'error':'invalid format'}), 500 


# @app.route('/remove/<int:id>', methods = ['DELETE'])
# def remove(id):
# 	# TODO Add you code here.
	
# 	remove_item(id)

# 	return jsonify({'todo_list':todos}), 200 

# @app.route('/list', methods = ['GET'])
# def list():
# 	return jsonify({'todo_list':todos}), 200

# if __name__ == '__main__':
# 	app.debug = True
# 	app.run()