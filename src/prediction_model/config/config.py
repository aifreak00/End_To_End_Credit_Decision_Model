import pathlib
import os
import prediction_model

PACKAGE_ROOT = pathlib.Path(prediction_model.__file__).resolve().parent

DATAPATH = os.path.join(PACKAGE_ROOT, "datasets")

TRAIN_FILE = "train.csv"
TEST_FILE = "test.csv"

MODEL_NAME = "RandomForestClassifier.pkl"
SAVE_MODEL_PATH = os.path.join(PACKAGE_ROOT, "trained_models")

TARGET = "loan_status"

# Final features used in the model
FEATURES = ["rate", "amount", "purpose", "period", "cus_age", "gender",
       "education_level", "marital_status", "has_children", "living_situation",
       "total_experience", "job_sector", "DTI", "APR",
       "ccr_tot_mounth_amt", "ccr_payed_loan_tot_amt",
       "ccr_act_loan_tot_rest_amt", "income"]


NUM_FEATURES = ["rate", "amount", "period", "cus_age", "total_experience",
 "ccr_act_loan_tot_rest_amt", "DTI", "APR", "ccr_tot_mounth_amt",
 "ccr_payed_loan_tot_amt", "income"]


CAT_FEATURES = ["purpose", "gender", "education_level", "marital_status",
                 "has_children", "living_situation", "job_sector"]


# In our case it is same as Categorical features
FEATURES_TO_ENCODE = ["purpose", "gender", "education_level", "marital_status",
                 "has_children", "living_situation", "job_sector"]


# Feature engineering transformations
INCOME_COLUMN = "income"
ANNUAL_MULTIPLIER = 12
AMOUNT_COLUMN = "amount"
NEW_ANNUAL_INCOME_COLUMN = "annual_income"
NEW_INCOME_TO_LOAN_RATIO_COLUMN = "income_to_loan_ratio"
COLUMNS_TO_DROP = ["income"]


# Log transformation configuration
LOG_TRANSFORM_CONSTANT = 1e-6
NUMERICAL_COLUMNS = ["rate", "amount", "period", "cus_age", "total_experience",
 "ccr_act_loan_tot_rest_amt", "DTI", "APR", "ccr_tot_mounth_amt",
 "ccr_payed_loan_tot_amt", "annual_income","income_to_loan_ratio"]