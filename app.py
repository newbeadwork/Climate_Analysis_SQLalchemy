import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



# Creating 'engine'

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# #Creating Base variable 
Base = automap_base()
Base.prepare(engine, reflect=True)

# Saving references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Creating Flask
app = Flask(__name__)

#Setting routes

@app.route("/")
def home():
    """List all available api-routes."""
    return (
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
     )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Creating session 
    session = Session(engine)

    """Return precipitation by date"""
    # Quering data on date and precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Creating a dictionary from the precipitation data 
    daily_precipitation = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["precipitation"] = prcp
        daily_precipitation.append(prcp_dict)

    return jsonify(daily_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Creating session 
    session = Session(engine)

    """List of stations"""
    
    # Quering data on stations
    results = session.query(Station.name).all()

    session.close()

    # Creating a list from stations data 
    list_stations = []
    for name in results:
        list_stations.append(name)

    return jsonify(list_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Creating session 
    session = Session(engine)

    """Temperature observations for the most active station for the last year"""
    # Quering data on most active station
    
    chosen_data = [Measurement.station, 
       func.count(Measurement.id)]
    active_station = session.query(*chosen_data).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.id).desc()).first()
    
    
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == active_station[0]).\
        filter(Measurement.date > '2016-08-23').all()

    session.close()

    # Creating a list of temperature observations for the last year of the data 
    list_temperatures = []
    for tobs in results:
        list_temperatures.append(tobs)

    return jsonify(list_temperatures)

if __name__ == '__main__':
    app.run(debug=True)
