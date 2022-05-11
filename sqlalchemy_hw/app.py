import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#############################################
#Database setup
############################################

engine = create_engine("sqlite///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )
@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a list of all precipitation and date"""
    # Query all precipitation and date
    results = session.query(Measurement.date,Measurement.prcp).all()

    session.close()
    
     # Convert list of tuples into dictionary
    total_precepitation=[]
    for date,prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        total_precepitation.append(precipitation_dict)

    return jsonify(total_precepitation)
    
    
@app.route("/api/v1.0/stations")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.id,Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).all()
    session.close()
    
    # Convert list of tuples into dictionary
    all_station=[]
    for id,station,name,latitude,longitude,elevation in results:
        station_dict={}
        station_dict['Id']=id
        station_dict['station']=station
        station_dict['name']=name
        station_dict['latitude']=latitude
        station_dict['longitude']=longitude
        station_dict['elevation']=elevation
        all_station.append(station_dict)
    
    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tempartureobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    
    
    
    
    
    
    
    
    
    
    
    
    