from flask import Flask, render_template, request 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://localhost/ipark'
db = SQLAlchemy(app)

from app import views