# Importing datatypes
from sqlalchemy import DateTime, Integer, Column, Float

# Model creation class
from sqlalchemy.ext.declarative import declarative_base

# Initiating the base class
Base = declarative_base()


# Defining the database models
class VilniusWeatherData(Base):
    """
    Aggregated information about the Sodra employees
    """
    __tablename__ = 'vilnius_weather_data'

    # Defining the columns needed 
    id = Column(Integer, primary_key=True)
    dt = Column(DateTime, index=True)
    temp = Column(Float)
    pressure = Column(Float)
    humidity = Column(Float)
    clouds = Column(Float)
    wind_speed = Column(Float)
    wind_deg = Column(Float) 
    hour_sin = Column(Float)
    hour_cos = Column(Float)
    month_sin = Column(Float)
    month_cos = Column(Float)