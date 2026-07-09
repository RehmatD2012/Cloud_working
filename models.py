from sqlalchemy import Column,Integer,Float,String
from database import Base

class HousePrediction(Base):

    __tablename__="house_predictions"

    id = Column(Integer,primary_key=True,index=True)

    housing_median_age = Column(Float)

    total_rooms = Column(Float)

    total_bedrooms = Column(Float)

    population = Column(Float)

    households = Column(Float)

    median_income = Column(Float)

    ocean_proximity = Column(String)

    predicted_price = Column(Float)