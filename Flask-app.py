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

#(First Route): Query for the dates and temperature observations from the last year; return the result as json representation 
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the dates and temperature observations from the last year"""
    # Query all dates and thier temperature
    results = session.query(Measurement.date,Measurement.tobs).\
                            filter(func.strftime("%y", Measurement.date) == "2017").all()

    # Create a dictionary from the row data and append to a list of last_year_tobs
    last_year_tobs = []
    for tobs in date_tobs_dict = {}
        date_tobs_dict["date"] = Measurement.date
        date_tobs_dict["tobs"] = Measurement.tobs
        
        last_year_tobs.append(date_tobs_dict)

    return jsonify(last_year_tobs)







if __name__ == '__main__':
    app.run(debug=True)





