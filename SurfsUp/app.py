# Import the dependencies.
import sqlalchemy
import datetime as dt
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurements = Base.classes.measurement
Stations = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# Homepage
@app.route("/")
def homepage():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# Precipitation for the past year (Date from climate_starter)
@app.route("/api/v1.0/precipitation")
def precipitation_func():
    session = Session(engine)
    results = session.query(Measurements.date, Measurements.prcp).filter(Measurements.date >= (dt.date(2017, 8, 23) - dt.timedelta(days=365)))
    session.close()

    prcp_last_year=[]
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_last_year.append(prcp_dict)

    return prcp_last_year

# All stations
@app.route("/api/v1.0/stations")
def stations_func():
    session = Session(engine)
    results = session.query(Stations.station).all()
    session.close()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

# Date and precipitation for the past year for the most active station (Date and station id from climate_starter)
@app.route("/api/v1.0/tobs")
def tobs_func():
    session = Session(engine)
    results = session.query(Measurements.date, Measurements.tobs).filter(Measurements.date >= (dt.date(2017, 8, 23) - dt.timedelta(days=365)), Measurements.station == 'USC00519281').all()
    session.close()
    all_tobs = list(np.ravel(results))
    return jsonify(all_tobs)

# Min, max, and avg temperature from specified start date until end (format: YYYY-MM-DD)
@app.route("/api/v1.0/<start>")
def start_func(start):
    session = Session(engine)
    results = session.query(func.min(Measurements.tobs),func.max(Measurements.tobs),func.avg(Measurements.tobs)).filter(Measurements.date >= start).all()
    session.close()
    temp_info_from_start = list(np.ravel(results))
    return jsonify(temp_info_from_start)

# Min, max, and avg temperature from specified start date to specified end date (format: YYYY-MM-DD)
@app.route("/api/v1.0/<start>/<end>")
def between_func(start,end):
    session = Session(engine)
    results = session.query(func.min(Measurements.tobs),func.max(Measurements.tobs),func.avg(Measurements.tobs)).filter(Measurements.date >= start, Measurements.date <= end ).all()
    session.close()
    temp_info_between = list(np.ravel(results))
    return jsonify(temp_info_between)

if __name__ == '__main__':
    app.run(debug=True)

