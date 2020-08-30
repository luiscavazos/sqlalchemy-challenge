import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#inspector = inspect(engine)
#columns = inspector.get_columns('measurement')
#for column in columns:
#    print(column["name"], column["type"])

#columns = inspector.get_columns('station')
#for column in columns:
#    print(column["name"], column["type"])


app = Flask(__name__)

@app.route("/")
def home():
    return("/api/v1.0/precipitation</br>"
    "/api/v1.0/stations</br>"
    "/api/v1.0/tobs</br>"
    "/api/v1.0/08-21-2016</br>"
    "/api/v1.0/08-21-2016/08-26-2016</br>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    result_p= session.query(Measurement.date, Measurement.prcp).filter(func.strftime("%Y-%m", Measurement.date) >= "2016-08").\
                          group_by(Measurement.date).order_by(Measurement.date).all()  
    prec_dic= list(np.ravel(result_p))
    return jsonify(prec_dic)

@app.route("/api/v1.0/stations")
def stations():
    result_st= session.query(Station.station, Station.name).all()
    stat_dic=list(np.ravel(result_st))
    return jsonify(stat_dic)

@app.route("/api/v1.0/tobs")
def tobs():
    result_tobs= session.query(Measurement.date, Measurement.tobs).filter(func.strftime("%Y-%m", Measurement.date) >= "2016-08").\
    filter(Measurement.station == 'USC00519281').all()
    tobs_dic=list(np.ravel(result_tobs))
    return jsonify(tobs_dic)

@app.route("/api/v1.0/08-21-2016")
def start():
    result_start= session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(func.strftime("%Y-%M-%D", Measurement.date) >= "2016-08-21")
    start_dic=list(np.ravel(result_start))
    return jsonify(start_dic)

@app.route("/api/v1.0/08-21-2016/08-26-2016")
def start_end():
    result_start_end= session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(func.strftime("%Y-%M-%D", Measurement.date) >= "2016-08-21").filter(func.strftime("%Y-%M-%D", Measurement.date) >= "2016-08-26")
    start_end_dic=list(np.ravel(result_start_end))
    return jsonify(start_end_dic)


if __name__ == '__main__':
    app.run(debug=True)