import pytest
from prediction_model.config import config
from prediction_model.processing.data_handling import load_dataset
from prediction_model.predict import generate_predictions


@pytest.fixture
def single_prediction():
    # Load a single example from the test dataset
    test_data = load_dataset(config.TEST_FILE)
    single_row = test_data.head(1).to_dict(orient="records")  # Convert to dict for generate_predictions
    result = generate_predictions(single_row)
    return result

def test_single_pred_not_none(single_prediction):
    # Check that the prediction result is not None
    assert single_prediction is not None

def test_single_pred_str_type(single_prediction):
    # Check that the prediction is of type str (e.g., "Approved" or "Rejected")
    predictions = single_prediction.get("Predictions")
    assert predictions is not None and isinstance(predictions[0], str)

def test_single_pred_validate(single_prediction):
    # Check that the prediction for the test data is "Approved"
    predictions = single_prediction.get("Predictions")
    assert predictions[0] == "Approved"