import pandas as pd
import numpy as np
import joblib
from prediction_model.config import config
from prediction_model.processing.data_handling import load_pipeline, load_dataset


model_pipeline = load_pipeline(config.MODEL_NAME)

def generate_predictions(data_input):
    # Convert the input data to a DataFrame
    data = pd.DataFrame(data_input)
    
    # Use the model pipeline to predict using the specified features from the input data
    predictions = model_pipeline.predict(data[config.FEATURES])
    
    # Convert numerical predictions to "Rejected" or "Approved"
    output = np.where(predictions == 1, "Rejected", "Approved")
    
    # Format the result as a dictionary
    result = {"Predictions": output}
    
    return result


# # For Preliminary testing
# def generate_predictions():
#     test_data = load_dataset(config.TEST_FILE)
#     predictions = model_pipeline.predict(test_data[config.FEATURES])
#     # Convert numerical predictions to "Rejected" or "Approved"
#     output = np.where(predictions == 1, "Rejected", "Approved")
#     # Format the result as a dictionary
#     # result = {"Predictions": output}
#     print(output)
#     return output


if __name__=="__main__":
    generate_predictions()