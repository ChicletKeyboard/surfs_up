# import dependencies
import datetime as dt 
import numpy as np 
import pandas as pd 

# dependencies for SQAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, session
from sqlalchemy import create_engine, func 

from flask import Flask, json, jsonify

# Set up database
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
## Reflect the database
Base.prepare(engine, reflect=True)
## Save refeerences to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
## Create session link from Python to database
session = Session(engine)

# Setup Flask application
## Using __name__ varriable depends on where code is run
## ex: running on app.py will set it to __main__ indicates not using any other file to run the code
app = Flask(__name__)
# Set welcome route and other routes in f-string
@app.route("/")
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# Crate precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Create stations rroute
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    # Convert results into 1-dimensional array --> then to a list
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Monthly temperature route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    # set date from previous year of Aug. 23, 2017
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # query primpary station for all temp observations since prev_year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    # unravel reuslts into 1-dimensional array --> convert to list
    temps = list(np.ravel(results))
    return jsonify(temps = temps)

# Route for statistical analysis
## Min/max/avg temperatures
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>") # need start and end date
def stats(start=None, end=None):
    # query to get min, avg, max temperatures
    ## Create list 'sel' with ^
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    ## need to determine start and end date so add if-not statement
    if not end:
        ## the asterik indicates multiple results for query (min/avg/max)
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        ## Convert results into 1-dimensional arrray --> then into list
        temps = list(np.ravel(results))
        return jsonify(temps = temps)

    ## Calcualte min, avg, max temp with start and end dates
    results = session.query(*sel).\
        filter(Measurement.date >= end).all()
    ## Convert results into 1-dimensional arrray --> then into list
    temps = list(np.ravel(results))
    return jsonify(temps = temps)
