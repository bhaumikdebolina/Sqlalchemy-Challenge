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

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
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
def precipitation():
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
def stations():
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
    
    """Return a list of all temparture observation"""
    # Calculate the date 1 year ago from the last data point in the database
    results_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    str_date=list(np.ravel(results_date))[0]
    latest_date=dt.datetime.strptime(str_date,"%Y-%m-%d")
    year_ago=latest_date-dt.timedelta(days=365)
    
    
    results=session.query(Measurement.date, Measurement.tobs).order_by(Measurement.date.desc()).\
            filter(Measurement.date>=year_ago).all()
    session.close()
    
    all_temperature=[]
    for tobs,date in results:
        tobs_dict={}
        tobs_dict['date']=date
        tobs_dict['tobs']=tobs
        all_temperature.append(tobs_dict)
    return jsonify(all_temperature)


# `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range.
# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than or equal to the start date.
# When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates from the start date through the end date (inclusive).
  
@app.route("/api/v1.0/<start>")
def temp_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    session.close()
     
    temp_obs={}
    temp_obs["Min_Temp"]=query[0][0]
    temp_obs["avg_Temp"]=query[0][1]
    temp_obs["max_Temp"]=query[0][2]
    return jsonify(temp_obs)

@app.route("/api/v1.0/<start>/<end>")
def temp(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    start_end_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),   
                     func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()
    
    
    temp_obs={}
    temp_obs["Min_Temp"]=start_end_temp[0][0]
    temp_obs["avg_Temp"]=start_end_temp[0][1]
    temp_obs["max_Temp"]=start_end_temp[0][2]
    return jsonify(temp_obs)
 
    return jsonify(start_end_temp)
    
if __name__ == "__main__":
    app.run(debug=True)
    
    
    
    
    
    
    
    
    
    
    