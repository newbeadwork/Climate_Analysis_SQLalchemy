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




if __name__ == '__main__':
    app.run(debug=True)
