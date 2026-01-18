import pandas as pd
from fastapi import FastAPI, HTTPException

from app.model import model   # this should be your MODEL or PIPELINE
from app.schema import PredictionRequest, PredictionResponse

app = FastAPI(
    title="Housing Price Prediction API",
    description="Predict house prices using a trained ML model",
    version="1.0.0"
)

# ✅ Column order (must match training data)
COLUMNS = [
    "longitude",
    "latitude",
    "housing_median_age",
    "total_rooms",
    "total_bedrooms",
    "population",
    "households",
    "median_income",
    "ocean_proximity",
]

# -------------------------
# Root endpoint (NO MORE 404)
# -------------------------
@app.get("/")
def home():
    return {
        "message": "Housing Price Prediction API is running",
        "usage": "Go to /docs to test the API"
    }


# -------------------------
# Prediction endpoint
# -------------------------
@app.post("/predict", response_model=PredictionResponse)
def predict(data: PredictionRequest):

    try:
        # Convert request → DataFrame
        df = pd.DataFrame([data.dict()], columns=COLUMNS)

        # Model / Pipeline prediction
        prediction = model.predict(df)

        return PredictionResponse(
            prediction=float(prediction[0])
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )
