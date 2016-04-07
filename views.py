from app import app, db 
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy 
#from sqlalchemy import text, create_engine 
import googlemaps
import json
from datetime import datetime
from flask_googlemaps import GoogleMaps

gmaps = googlemaps.Client(key='AIzaSyDyIjazEKwGObz96R856yDFMuNJJXXPzyU') 

#engine = create_engine('postgresql://localhost/ipark')

class Users(db.Model): 
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(80))
	email = db.Column(db.String(120), unique=True)
	firstName = db.Column(db.String(50)) 
	lastName = db.Column(db.String(50))
	role = db.Column(db.String(20))
	address = db.relationship('Spaces', backref='users', lazy='dynamic')

	def __init__(self, username, password, email, firstName, lastName, role): 
		self.username = username
		self.password = password
		self.email = email 
		self.firstName = firstName
		self.lastName = lastName 
		self.role = role 

	def __repr__(self): 
		return '<User %r>' % self.username 

class Spaces(db.Model): 
	id = db.Column(db.Integer, primary_key=True) 
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	address = db.Column(db.String(200))
	is_taken = db.Column(db.Boolean) 

	def __init__(self, user_id, address, is_taken):
		self.user_id = user_id 
		self.address = address
		self.is_taken = is_taken 

	def __repr__(self): 
		return '<Spaces %r>' % self.address 

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/map')
def map():
	return render_template('map.html')

@app.route('/signup')
def signup(): 
	return render_template('add_user.html')

@app.route('/post_user', methods=['POST']) 
def post_user(): 
	user = Users(request.form['username'],request.form['password'], request.form['email'], request.form['firstName'], request.form['lastName'], request.form['role'])
	db.session.add(user)
	db.session.commit() 
	return redirect(url_for('map')) 

@app.route('/get_spaces', methods=['GET', 'POST'])
def get_spaces(): 
	place = request.form['address'] 
	result = Spaces.query.all() 
	spaces = []
	for s in result: 
		spaces.append(s.address)
	#address = ["223 Adams street, Boston", "37 Buswell street, Boston","22 cummington mall, Boston","232 bay state road, Boston","975 Gaffney road, Boston","2 bay state Road, Boston"]
	locations = setLocation(place, spaces)
	return render_template('test.html', locations=locations)


    #CREATE_ENGINE 
	# sql = text('select address from Spaces where is_taken = false')
	# result = db.engine.execute(sql)
	# spaces = [] 
	# for s in spaces: 
	# 	spaces.append(row[0])

def setLocation(loc, geo):
	close = 5                    #close is our variable for what constitutes close to the guy wanting to park, it's 
	geoSpaces = geo               #set to 1 kilometre for now, but we might want to do something better than hardcoding that distance
	#geoSpaces = []    					# stubbed because of mysterious fucking inability to typecast string to float
	spaces = geo
	# for i in range(len(spaces)):
	# 	distance = gmaps.distance_matrix(loc, spaces[i])
	# 	km = distance['rows'][0]['elements'][0]['distance']['text']
	# 	km = km[:-3]
	#	km = float(km.replace(',','')) 
	# 	if km < close:
	# 		geoSpaces.append(spaces[i])
	# closeSpaces = []
	closeSpaces = []
	#print geoSpaces
	for j in range(len(geoSpaces)):
		geocode_result = gmaps.geocode(geoSpaces[j])
		#print geocode_result
		lat = geocode_result[0]['geometry']['location']['lat']
		lng = geocode_result[0]['geometry']['location']['lng']
		closeSpaces.append([lat,lng, geoSpaces[j]])

	#closeSpacesDict = {}
	closeSpacesList = []
	for i in closeSpaces:
		rabbit = {}
		rabbit['lat'] = i[0]
		rabbit['lng'] = i[1]
		rabbit['name'] = i[2]
		#closeSpacesDict[i[2]] = rabbit
		closeSpacesList.append(rabbit)
	
	ll = []
	for i in closeSpaces:
		ll.append([i[0],i[1]])  

	return ll

	







