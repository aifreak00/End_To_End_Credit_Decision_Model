import os
import pandas as pd
import joblib
from prediction_model.config import config

# Load the dataset
def load_dataset(file_name):
    filepath = os.path.join(config.DATAPATH, file_name)
    _data = pd.read_csv(filepath)
    return _data 

# Serialization
def save_pipeline(model, save_model_path):
    joblib.dump(model, save_model_path)
    print(f"Model has been saved at {save_model_path}")

# Deserialization
def load_pipeline(pipeline_to_load):
    save_path = os.path.join(config.SAVE_MODEL_PATH, config.MODEL_NAME)
    model_loaded = joblib.load(save_path)
    print(f"Model has been loaded")
    return model_loaded