import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from prediction_model.config import config
from prediction_model.processing.data_handling import load_dataset, save_pipeline
from prediction_model.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import os

# Initialize models and their grid search parameters
models = [
    {"name": "LogisticRegression", "model": LogisticRegression(random_state=42), "params": {"classifier__C": [0.1, 1.0, 10.0]}},
    {"name": "RandomForestClassifier", "model": RandomForestClassifier(random_state=42), "params": {"classifier__n_estimators": [10, 100, 200]}},
    {"name": "DecisionTreeClassifier", "model": DecisionTreeClassifier(random_state=42), "params": {"classifier__max_depth": [3, 5, 7]}}
]

def run_training():
    # Load and split dataset
    data = load_dataset(config.TRAIN_FILE)
    X, y = data[config.FEATURES], data[config.TARGET]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    for model_info in models:
        pipeline = make_pipeline(model_info["model"])
        grid_search = GridSearchCV(pipeline, param_grid=model_info["params"], cv=5, scoring='accuracy')
        grid_search.fit(X_train, y_train)

        best_model = grid_search.best_estimator_
        predictions = best_model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        f1 = f1_score(y_test, predictions)
        roc_auc = roc_auc_score(y_test, predictions)

        # Print metrics to the console
        print(f"Results for {model_info['name']}:")
        print(f"Best Params: {grid_search.best_params_}")
        print(f"Accuracy: {accuracy}")
        print(f"F1 Score: {f1}")
        print(f"ROC AUC: {roc_auc}")

        # Save the best models locally
        save_model_path = os.path.join(config.SAVE_MODEL_PATH, f"{model_info['name']}.pkl")
        save_pipeline(best_model, save_model_path)

if __name__ == "__main__":
    run_training()
