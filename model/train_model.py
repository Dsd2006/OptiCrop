
import pandas as pd
import joblib
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "dataset" / "crop_data.csv"
MODEL_PATH = Path(__file__).resolve().parent / "crop_model.pkl"

# Required input features
FEATURES = [
    "nitrogen",
    "phosphorus",
    "potassium",
    "temperature",
    "humidity",
    "ph",
    "rainfall"
]


def train_model():

    print("\n🌱 OPTICROP - AI MODEL TRAINING")
    print("=" * 45)

    # Check dataset
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    print("\nLoading crop dataset...")

    df = pd.read_csv(DATASET_PATH)

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Support common dataset column names
    column_mapping = {
        "n": "nitrogen",
        "nitrogen": "nitrogen",
        "p": "phosphorus",
        "phosphorus": "phosphorus",
        "k": "potassium",
        "potassium": "potassium",
        "temp": "temperature",
        "temperature": "temperature",
        "humidity": "humidity",
        "ph": "ph",
        "rainfall": "rainfall",
        "label": "crop",
        "crop": "crop",
        "crop_name": "crop",
        "recommended_crop": "crop"
    }

    df = df.rename(columns=column_mapping)

    # Validate columns
    required_columns = FEATURES + ["crop"]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing dataset columns: {missing}\n"
            f"Available columns: {list(df.columns)}"
        )

    # Clean dataset
    df = df[required_columns].copy()

    for column in FEATURES:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        )

    df["crop"] = df["crop"].astype(str).str.strip()

    df = df.dropna()
    df = df[df["crop"] != ""]

    if len(df) < 10:
        raise ValueError(
            "Dataset has too few valid rows. "
            "Please check crop_data.csv."
        )

    print(f"Dataset records: {len(df)}")
    print(f"Crop varieties: {df['crop'].nunique()}")

    # Prepare training data
    X = df[FEATURES]
    y = df["crop"]

    # Split dataset
    stratify_option = (
        y if y.value_counts().min() >= 2 else None
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=stratify_option
    )

    print("\nTraining AI model...")

    # Random Forest model
    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=15,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    # Evaluate model
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print("\nMODEL TRAINING RESULTS")
    print("-" * 45)
    print(f"Training records: {len(X_train)}")
    print(f"Testing records: {len(X_test)}")
    print(f"Model Accuracy: {accuracy * 100:.2f}%")

    print("\nClassification Report:")
    print(classification_report(
        y_test,
        predictions,
        zero_division=0
    ))

    # Save trained model
    joblib.dump(model, MODEL_PATH)

    print("\nAI model saved successfully!")
    print(f"Model location: {MODEL_PATH}")
    print("\n🌱 OPTICROP MODEL TRAINING COMPLETED!")
    print("=" * 45)


if __name__ == "__main__":
    train_model()
