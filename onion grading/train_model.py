import os
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from extract_features import extract_features


DATASET_PATH = "data"

GRADES = [
    "grade_A",
    "grade_B",
    "grade_C"
]


X = []
y = []


print("\n================================")
print("      ONIONSETU MODEL TRAINING")
print("================================\n")


# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

for grade in GRADES:

    folder = os.path.join(
        DATASET_PATH,
        grade
    )

    if not os.path.exists(folder):

        print(
            f"WARNING: {folder} not found"
        )

        continue

    files = [
        f
        for f in os.listdir(folder)
        if f.lower().endswith(
            (".jpg", ".jpeg", ".png")
        )
    ]

    print(
        f"{grade}: {len(files)} images"
    )

    for filename in files:

        path = os.path.join(
            folder,
            filename
        )

        try:

            features = extract_features(
                path
            )

            X.append(features)
            y.append(grade)

        except Exception as error:

            print(
                f"Skipping {filename}: {error}"
            )


if len(X) == 0:

    raise RuntimeError(
        "No training images found."
    )


# --------------------------------------------------
# TRAIN / TEST SPLIT
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# --------------------------------------------------
# RANDOM FOREST
# --------------------------------------------------

model = RandomForestClassifier(

    n_estimators=300,

    max_depth=15,

    min_samples_split=3,

    min_samples_leaf=2,

    random_state=42,

    class_weight="balanced"

)


print("\nTraining model...\n")

model.fit(
    X_train,
    y_train
)


# --------------------------------------------------
# EVALUATION
# --------------------------------------------------

predictions = model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(
    f"\nTest Accuracy: {accuracy:.2%}"
)


print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions
    )
)


print("\nConfusion Matrix:")
print(
    confusion_matrix(
        y_test,
        predictions
    )
)


# --------------------------------------------------
# FEATURE IMPORTANCE
# --------------------------------------------------

feature_names = [

    "Object Area",
    "Object Perimeter",
    "Circularity",
    "Average Hue",
    "Average Saturation",
    "Average Brightness",
    "Brightness Variation",
    "Dark Spot Count",
    "Dark Spot Ratio",
    "Edge Density"

]


print("\nFeature Importance:")

for name, importance in zip(
    feature_names,
    model.feature_importances_
):

    print(
        f"{name:25s}: "
        f"{importance:.4f}"
    )


# --------------------------------------------------
# SAVE MODEL
# --------------------------------------------------

joblib.dump(
    model,
    "onion_model.pkl"
)


print(
    "\nModel saved as onion_model.pkl"
)

print("\nTraining completed successfully.")