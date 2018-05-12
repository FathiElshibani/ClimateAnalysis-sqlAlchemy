# import the required libraries 
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify




# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)


# Flask Setup
app = Flask(__name__)





# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"    )

#(First Route): Return a json list of temperature observations from the last year.
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the dates and temperature observations from the last year"""
    # Query all dates and thier temperature
    results = session.query(Measurement.date,Measurement.tobs).\
                            filter(func.strftime("%y", Measurement.date) == "2017").all()

    # Create a dictionary from the row data and append to a list of last_year_tobs
    last_year_tobs = []
    for tobs in results:
        date_tobs_dict = {}
        date_tobs_dict["date"] = Measurement.date
        date_tobs_dict["tobs"] = Measurement.tobs
        
        last_year_tobs.append(date_tobs_dict)

    return jsonify(last_year_tobs)


#(Second Route): Return a json list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    """Return list of stations"""
    # Query to return list of stations
    results = session.query(Station.station,Station.name).all()

    # Create a dictionary from the row data and append to a list of stations_list
    stations_list = []
    for s in results: 
        stations_dict = {}
        stations_dict["station"] = Station.station
        stations_dict["name"] = Station.name
        
        stations_list.append(stations_dict)

    return jsonify(stations_list)


#(Third Route): Return a json list of Temperature Observations (tobs) for the previous year. 
@app.route("/api/v1.0/<start>")
def tobs_startDate():
    """Return list of Temperature Observations"""
    # Query to return llist of Temperature Observations (tobs) for the previous year
    results = session.query(Measurement.date, Measurement.tobs.label('Observated Temperature').\
                                     filter(func.strftime("%y", Measurement.date) == 2017).all())

    # Create a dictionary from the row data and append to a list of temperature observations list
    tobs_list = []
    for t in results: 
        tobs_dict = {}
        tobs_dict["Temperature Observations"] = Measurement.tobs
        
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)


#(Forth Route):
@app.route("/api/v1.0/<start>")
def Year_temps(start_date):
     return results = session.query(func.avg(Measurement.tobs).label('tobs_averge'), 
                                    func.max(Measurement.tobs).label('tobs_highest'), 
                                    func.min(Measurement.tobs).label('tobs_lowest')).\
                                    filter(func.strftime('%Y-%m-%d', Measurement.date) == start_date).all()    

    tobsforDate_list = []
    for t in results: 
        tobs_dict = {}
        tobs_dict["Temperature Observations"] = Measurement.tobs
        
        tobsforDate_list.append(tobs_dict)

    return jsonify(tobsforDate_list)



#(Fifth Route):
@app.route("/api/v1.0/<start>/<end>")
def Year_temps(start_date,end_date):
     return results = session.query(func.avg(Measurement.tobs).label('tobs_averge'), 
                                    func.max(Measurement.tobs).label('tobs_highest'), 
                                    func.min(Measurement.tobs).label('tobs_lowest')).\
                                    filter(func.strftime('%Y-%m-%d', Measurement.date) <= end_date).\
                                    filter(func.strftime('%Y-%m-%d', Measurement.date) >= start_date).all()    

    tobsforYear_list = []
    for t in results: 
        tobs_dict = {}
        tobs_dict["Temperature Observations"] = Measurement.tobs
        
        tobsforYear_list.append(tobs_dict)

    return jsonify(tobsforYear_list)




if __name__ == '__main__':
    app.run(debug=True)





