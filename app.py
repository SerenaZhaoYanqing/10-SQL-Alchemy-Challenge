# import 
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt 

# database set up 
engine = create_engine("sqlite:///hawaii.sqlite")
connect_args={'check_same_thread': False}

#reflect existing databese into a new model , reflect the table 
base=automap_base()
base.prepare(engine, reflect=True)

# save reference to each table 
m = base.classes.measurement
s = base.classes.station

# Create our session (link) from Python to the DB
session=Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes
#################################################
#list all APIs 
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
     )

#################################################
#return jsonify results of date and prcp 
@app.route("/api/v1.0/precipitation")
def precipitation():
    # with previous activity, we have found the latest date is 2017-08-23
    # finding start date 
    start_date=dt.date(2017,8,23)-dt.timedelta(days=365)
    #perform query for the last year's data (prcp and date)
    results=session.query(m.prcp, m.date).filter(m.date>start_date).order_by(m.date).all()
    session.close()

    # Convert list of tuples into normal list
    date_prcp=list(np.ravel(results))
    return jsonify(date_prcp)

#################################################
#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    # using groupby and get a list of stations (result is already list, just need to jsonify )
    station_result=session.query(m.station).group_by(m.station).all()
    session.close()

    stations_list=list(np.ravel(station_result))
    return jsonify(stations_list)

#################################################
#Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    # from previous exercise we have already found the most active station USC00519281 
    start_date=dt.date(2017,8,23)-dt.timedelta(days=365)
    results=session.query(m.tobs,m.date).filter(m.station=="USC00519281").filter(m.date>start_date).order_by(m.date).all()
    session.close()
    date_temp=list(np.ravel(results))
    return jsonify(date_temp)
#################################################
@app.route("/api/v1.0/start")
def start ():
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# setting start date as : 2015-12-8
#getting min, average, max for all weather data that is greater than 2015.1208
    start_date=dt.date(2015,12,8)
    start_weather = session.query(func.min(m.tobs), func.avg(m.tobs), func.max(m.tobs)).filter(m.date >= start_date).all()
    session.close()
    start_weather_details= list(np.ravel(start_weather))
    return jsonify(start_weather_details)
#################################################
@app.route("/api/v1.0/start/end")
def calc_temps():
#hen given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
# setting start date as : 2015-12-8, end date as : 2015-12-25, using %Y-%m-%d format 
    start_date=dt.date(2015,12,8)
    end_date=dt.date(2015,12,25)
    start_end_weather = session.query(func.min(m.tobs), func.avg(m.tobs), func.max(m.tobs)).\
        filter(m.date >= start_date).filter(m.date <=end_date).all()
    session.close()
    start_end_weather_details= list(np.ravel(start_end_weather))
    return jsonify(start_end_weather_details)
#################################################

if __name__ == '__main__':
    app.run(debug=True)