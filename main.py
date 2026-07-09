from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import pandas as pd
import joblib

from database import Base,engine,get_db
from models import HousePrediction
from schemas import HouseInput,PredictionResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)

model = joblib.load("model.pkl")
encoder = joblib.load("label_encoder.pkl")


@app.post("/predict",response_model=PredictionResponse)
def predict(data:HouseInput,db:Session=Depends(get_db)):

    encoded = encoder.transform([data.ocean_proximity])[0]

    df = pd.DataFrame({
        "housing_median_age":[data.housing_median_age],
        "total_rooms":[data.total_rooms],
        "total_bedrooms":[data.total_bedrooms],
        "population":[data.population],
        "households":[data.households],
        "median_income":[data.median_income],
        "ocean_proximity":[encoded]
    })

    prediction = float(model.predict(df)[0])

    house = HousePrediction(
        housing_median_age=data.housing_median_age,
        total_rooms=data.total_rooms,
        total_bedrooms=data.total_bedrooms,
        population=data.population,
        households=data.households,
        median_income=data.median_income,
        ocean_proximity=data.ocean_proximity,
        predicted_price=prediction
    )

    db.add(house)
    db.commit()
    db.refresh(house)

    return {"predicted_price":prediction}