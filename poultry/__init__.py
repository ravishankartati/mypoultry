import os

from flask import Flask
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS, cross_origin

app = Flask(__name__, instance_relative_config=True)

# Define the WSGI application objectv
# CORS(app)
CORS(app)

# Configurations
app.config.from_object('config_poultry')

# Environment variables
# app.config.from_envvar('poultry.env')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Import a module / component using its blueprint handler variable (mod_auth)
from poultry.mod_auth.controllers import mod_auth as auth_module
from poultry.mod_shed.controllers import mod_shed as shed_module

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(shed_module)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

@app.route('/', methods=('GET', 'POST'))
def test():
    return "helllo"