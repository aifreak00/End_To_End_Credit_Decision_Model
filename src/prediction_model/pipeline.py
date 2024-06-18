from sklearn.pipeline import Pipeline
from prediction_model.config import config
import prediction_model.processing.preprocessing as pp 
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.base import clone
import numpy as np

def make_pipeline(classifier):
    pipeline = Pipeline(
        [
            ("mean_imputation", pp.MeanImputation(variables=config.NUM_FEATURES)),  
            ("mode_imputation", pp.ModeImputation(variables=config.CAT_FEATURES)), 
            ("custom_processing", pp.CustomProcessing()),  
            ("drop_features", pp.ColumnDropper(variables_to_drop=config.COLUMNS_TO_DROP)),
            ("label_encoder", pp.CategoricalEncoder(variables=config.FEATURES_TO_ENCODE)),
            ("log_scaling", pp.LogScaler(variables=config.NUMERICAL_COLUMNS, add_constant=True)),
            ("standard_scale", StandardScaler()), 
            ("classifier", clone(classifier))  # Dynamically insert classifier
        ]
    )
    return pipeline

