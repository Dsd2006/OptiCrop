
import joblib
import pandas as pd
from pathlib import Path


# Model location
MODEL_PATH = Path(__file__).resolve().parent / "crop_model.pkl"

FEATURES = [
    "nitrogen",
    "phosphorus",
    "potassium",
    "temperature",
    "humidity",
    "ph",
    "rainfall"
]


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "AI model not found. Please run train_model.py first."
        )

    return joblib.load(MODEL_PATH)


def predict_crop(data):

    # Check input values
    missing = [feature for feature in FEATURES if feature not in data]

    if missing:
        raise ValueError(f"Missing input values: {missing}")

    try:
        input_data = {
            feature: float(data[feature])
            for feature in FEATURES
        }
    except (TypeError, ValueError):
        raise ValueError("All input values must be numeric.")

    # Basic input validation
    if any(value < 0 for value in input_data.values()):
        raise ValueError("Input values cannot be negative.")

    if not 0 <= input_data["ph"] <= 14:
        raise ValueError("Soil pH must be between 0 and 14.")

    # Prepare input for prediction
    input_df = pd.DataFrame(
        [input_data],
        columns=FEATURES
    )

    # Load trained AI model
    model = load_model()

    # Predict crop
    predicted_crop = model.predict(input_df)[0]

    # Calculate model confidence
    probabilities = model.predict_proba(input_df)[0]
    confidence = float(max(probabilities)) * 100

    result = {
        "crop": str(predicted_crop).capitalize(),
        "confidence": round(confidence, 2),
        "message": (
            f"AI recommends {str(predicted_crop).capitalize()} "
            "based on the supplied soil and weather data."
        )
    }

    return result


if __name__ == "__main__":

    sample_data = {
        "nitrogen": 90,
        "phosphorus": 42,
        "potassium": 43,
        "temperature": 25,
        "humidity": 80,
        "ph": 6.5,
        "rainfall": 200
    }

    try:
        result = predict_crop(sample_data)

        print("\n🌱 OPTICROP - CROP PREDICTION")
        print("=" * 40)
        print("Recommended Crop:", result["crop"])
        print("Model Confidence:", result["confidence"], "%")
        print(result["message"])
        print("=" * 40)

    except (ValueError, FileNotFoundError) as error:
        print("Prediction Error:", error)
