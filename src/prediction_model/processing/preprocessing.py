from sklearn.base import BaseEstimator,TransformerMixin
from prediction_model.config import config
import numpy as np

class MeanImputation(BaseEstimator,TransformerMixin):
    def __init__(self,variables=None):
        self.variables = variables
    
    def fit(self,X,y=None):
        self.mean_dict = {}
        for col in self.variables:
            self.mean_dict[col] = X[col].mean()
        return self
    
    def transform(self,X):
        X = X.copy()
        for col in self.variables:
            X[col].fillna(self.mean_dict[col],inplace=True)
        return X


class ModeImputation(BaseEstimator,TransformerMixin):
    def __init__(self,variables=None):
        self.variables = variables
    
    def fit(self,X,y=None):
        self.mode_dict = {}
        for col in self.variables:
            self.mode_dict[col] = X[col].mode()[0]
        return self
    
    def transform(self,X):
        X = X.copy()
        for col in self.variables:
            X[col].fillna(self.mode_dict[col],inplace=True)
        return X

class ColumnDropper(BaseEstimator,TransformerMixin):
    def __init__(self,variables_to_drop=None):
        self.variables_to_drop = variables_to_drop
    
    def fit(self,X,y=None):
        return self
    
    def transform(self,X):
        X = X.copy()
        X = X.drop(columns = self.variables_to_drop)
        return X


class CustomProcessing(BaseEstimator, TransformerMixin):
    def __init__(self):
        # No need for variables in the initializer since we're using config
        pass
    
    def fit(self, X, y=None):
        # No fitting necessary for this transformation
        return self
    
    def transform(self, X):
        X = X.copy()
        
        # Convert monthly income to annual income
        X[config.NEW_ANNUAL_INCOME_COLUMN] = X[config.INCOME_COLUMN] * config.ANNUAL_MULTIPLIER
        
        # Creating Income to Loan Amount ratio column
        X[config.NEW_INCOME_TO_LOAN_RATIO_COLUMN] = X[config.NEW_ANNUAL_INCOME_COLUMN] / X[config.AMOUNT_COLUMN]
   
        return X


class CategoricalEncoder(BaseEstimator,TransformerMixin):
    def __init__(self, variables=None):
        self.variables=variables
    
    def fit(self, X,y):
        self.label_dict = {}
        for var in self.variables:
            t = X[var].value_counts().sort_values(ascending=True).index 
            self.label_dict[var] = {k:i for i,k in enumerate(t,0)}
        return self
    
    def transform(self,X):
        X=X.copy()
        for feature in self.variables:
            X[feature] = X[feature].map(self.label_dict[feature])
        return X


# Log Transformation

class LogScaler(BaseEstimator, TransformerMixin):
    def __init__(self, variables=None, add_constant=True):
        if variables is None:
            self.variables = config.NUMERICAL_COLUMNS
        else:
            self.variables = variables
        self.add_constant = add_constant
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()
        for col in self.variables:
            if self.add_constant:
                X[col] = np.log(X[col] + config.LOG_TRANSFORM_CONSTANT)
            else:
                X[col] = np.log(X[col])
        return X