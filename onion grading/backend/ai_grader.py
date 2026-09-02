import sys
from pathlib import Path

import joblib

# Allow backend to access files in the main project folder
BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(BASE_DIR))

from extract_features import extract_features


MODEL_PATH = BASE_DIR / "onion_model.pkl"


def load_model():

    if not MODEL_PATH.exists():

        raise FileNotFoundError(
            "onion_model.pkl was not found."
        )

    return joblib.load(MODEL_PATH)


def grade_onion(image_path):

    # Load trained model
    model = load_model()

    # Extract features from image
    features = extract_features(
        str(image_path)
    )

    # Predict grade
    prediction = model.predict(
        [features]
    )[0]

    # Get confidence
    probabilities = model.predict_proba(
        [features]
    )[0]

    confidence = float(
        max(probabilities)
    )

    # Convert grade_A -> A
    grade = prediction.replace(
        "grade_",
        ""
    )

    return {

        "grade": grade,

        "confidence": confidence,

        "features": features

    }