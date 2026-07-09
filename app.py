# Import Libraries
import streamlit as st
import requests

# FastAPI URL
API_URL = "http://127.0.0.1:8000/predict"

# Title
st.title("🏠 House Price Prediction")

st.write("Enter the house details below.")


# User Inputs

housing_median_age = st.number_input(
    "Housing Median Age",
    min_value=0,
    value=25
)

total_rooms = st.number_input(
    "Total Rooms",
    min_value=0,
    value=5
)

total_bedrooms = st.number_input(
    "Total Bedrooms",
    min_value=0,
    value=5
)

population = st.number_input(
    "Population",
    min_value=0,
    value=1200
)

households = st.number_input(
    "Households",
    min_value=0,
    value=5
)

median_income = st.number_input(
    "Median Income",
    min_value=0,
    value=4
)

ocean_proximity = st.selectbox(
    "Ocean Proximity",
    [
        "<1H OCEAN",
        "INLAND",
        "ISLAND",
        "NEAR BAY",
        "NEAR OCEAN"
    ]
)

# Prediction

if st.button("Predict House Price"):

    data = {
        "housing_median_age": housing_median_age,
        "total_rooms": total_rooms,
        "total_bedrooms": total_bedrooms,
        "population": population,
        "households": households,
        "median_income": median_income,
        "ocean_proximity": ocean_proximity
    }

    try:
        response = requests.post(API_URL, json=data)

        if response.status_code == 200:
            result = response.json()

            st.success(
                f"🏠 Estimated House Price: ${result['predicted_price']:,.2f}"
            )

        else:
            st.error(f"Error {response.status_code}")
            st.write(response.json())

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the FastAPI server.")
        st.info("Make sure your FastAPI backend is running using:")
        st.code("uvicorn main:app --reload")

    except Exception as e:
        st.error(f"An error occurred: {e}")