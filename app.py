# import all libries required
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify
from sqlalchemy.sql import base


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database to a new model 
base = automap_base()

# reflect the tables 
base.prepare(engine, reflect=True)

#save reference to each table (measurement and station)
m = base.classes.measurement
s = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# list out all routes that are available
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>/<end>"
    )
#################################################
@app.route ("/api/v1.0/precipitation")
def precipitation():
 
    # Perform a query to retrieve the data and precipitation scores
    latest_date=session.query(m.date).order_by(m.date.desc()).first()
    start_date=dt.date(2017,8,23)-dt.timedelta(days=365)
    results=session.query(m.prcp,m.date).\
        filter(m.date > start_date).\
        order_by(m.date).all()
    # list comprehension the results
    date_prcp=[]
    for result in results:
        row= {}
        row["date"]=results[1]
        row["prcp"]=results[0]
        date_prcp.append(row)
    return jsonify (date_prcp)
#################################################
if __name__ == '__main__':
    app.run(debug=True)