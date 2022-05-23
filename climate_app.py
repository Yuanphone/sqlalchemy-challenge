import warnings
warnings.filterwarnings('ignore')
# Import Dependencies
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func,Float
from flask import Flask, jsonify
import datetime as dt
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base=automap_base()
Base.classes.keys()
# reflect the tables
Base.prepare(engine,reflect=True)
Measurement=Base.classes.measurement
Station=Base.classes.station
# # Flask Setup
#################################################
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"<b>Welcome to Climate API for Honolulu, Hawaii!</b><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitaion<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start=YYYY-MM-DD<br/>"
        f"/api/v1.0/start=YYYY-MM-DD/end=YYYY-MM-DD"
    )


@app.route("/api/v1.0/precipitaion")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Measurement.date,Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_prcp= []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)
    

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all stations
    results = session.query(Measurement.station,
                            Station.name,
                            Station.latitude,
                            Station.longitude,
                            Station.elevation,
                            func.min(Measurement.prcp),
                            func.max(Measurement.prcp),
                            func.avg(Measurement.prcp),
                            func.min(Measurement.tobs),
                            func.max(Measurement.tobs),
                            func.avg(Measurement.tobs))\
        .filter(Measurement.station == Station.station)\
        .group_by(Measurement.station).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station, name, latitude, longitude,elevation,min_prcp,max_prcp,avg_prcp,min_tobs,max_tobs,avg_tobs in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        station_dict["min_prcp"] = min_prcp
        station_dict["max_prcp"] = max_prcp
        station_dict["avg_prcp"] = avg_prcp
        station_dict["min_tobs"] = min_tobs
        station_dict["max_tobs"] = max_tobs
        station_dict["avg_tobs"]=avg_tobs
        
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query
    latest_date_query = session.query(Measurement.date).order_by(
        Measurement.date.desc()).first()
    latest_date_str = latest_date_query[0]
    latest_date = dt.datetime.strptime(latest_date_str, '%Y-%m-%d').date()

    # 1 year ago from the last data point
    query_date = latest_date - dt.timedelta(days=365)
    query_date_str = query_date.strftime('%Y-%m-%d')
    
    active_station=session.query(Measurement.station,Station.name)\
            .group_by(Measurement.station).\
            order_by(func.count(Measurement.station).desc()).first()
    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station==active_station[0]).\
            filter(Measurement.date>=query_date_str).all()
            # .filter(Measurement.date<=latest_date_str)
    session.close()

    # Convert list of tuples into normal list
    all_tobs= []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["Station ID"]=active_station[0]
        tobs_dict["Station Name"]=active_station[1]
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        all_tobs.append(tobs_dict)
    
    return jsonify(all_tobs)
@app.route("/api/v1.0/start=<start>")
def start(start):
    session = Session(engine)

    results=session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date>=start).all()
    last_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    first_date=session.query(Measurement.date).order_by(Measurement.date).first()
    session.close()
    daterange=pd.date_range(start=first_date[0],end=last_date[0])
    all_start=[]
    for TMIN,TAVG,TMAX in results:
        start_dict={}
        start_dict["Start Date"]=start
        start_dict["End Date"]=last_date[0]
        start_dict["TMIN"]=TMIN
        start_dict["TAVG"]=TAVG
        start_dict["TMAX"]=TMAX
        all_start.append(start_dict)
    if start in daterange:
        return jsonify(all_start)
    else:
        return jsonify({"error":f"Temperature on the date {start} not found.Date must be between {first_date[0]} and {last_date[0]}"}), 404
@app.route("/api/v1.0/start=<start>/end=<end>")
def start_end(start,end):
    session = Session(engine)

    results=session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    last_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    first_date=session.query(Measurement.date).order_by(Measurement.date).first()
    session.close()
    daterange=pd.date_range(start=first_date[0],end=last_date[0])
    start_end=[]
    for TMIN,TAVG,TMAX in results:
        period_dict={}
        period_dict["Start Date"]=start
        period_dict["End Date"]=end
        # period_dict = {
        #     'Start Date': start,
        #     'End Date': end
        # }
        period_dict["TMIN"]=TMIN
        period_dict["TAVG"]=TAVG
        period_dict["TMAX"]=TMAX
        start_end.append(period_dict)
    if start and end in daterange:
        return jsonify(start_end)
    else:
        return jsonify({"error":f"Temperatures between the start date {start} and {end} not found."}), 404
   
if __name__ == '__main__':
    app.run(debug=True)

