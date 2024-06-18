# Credit Decision Model Package

## Problem Statement

Financial institutions often face the challenge of making swift and accurate decisions on loan applications. The goal of this project is to automate the loan eligibility process, providing a predictive model that assesses the likelihood of a loan's approval based on customer-provided information. While the data used for model training and validation is synthetic, the scenario represents a realistic application within the banking sector.

Using machine learning, we aim to create a model that predicts the outcome of a loan application, enabling faster and more consistent decision-making. The model addresses key factors such as creditworthiness, financial stability, and loan repayment capability. Despite the dataset's synthetic nature, the methods and approaches applied here adhere to industry-standard practices for model development and evaluation, offering a valid demonstration of technical proficiency in a machine learning context.

## Data

The dataset included in this project is synthetic, designed to mimic real-world financial data related to loan applications. It has been carefully generated to reflect the characteristics and challenges one might expect from genuine banking datasets, without containing any sensitive personal information. The synthetic nature of the data ensures compliance with privacy laws and ethical standards. It serves as a tool for demonstrating data processing and machine learning capabilities in a controlled environment.


## Data Description

The following table provides details on the dataset's columns:

| Variable                      | Description                                                       |
| ----------------------------- | ----------------------------------------------------------------- |
| `customer_id`                 | A unique identifier for each customer.                            |
| `rate`                        | The interest rate of the loan, typically expressed as a percentage. |
| `amount`                      | The total amount of loan borrowed.                                |
| `purpose`                     | The reason or purpose for which the loan was taken.               |
| `period`                      | The duration over which the loan is to be repaid.                 |
| `cus_age`                     | The age of the customer.                                          |
| `gender`                      | The gender of the customer.                                       |
| `education_level`             | The highest level of education attained by the customer.          |
| `marital_status`              | The marital status of the customer (e.g., single, married).       |
| `has_children`                | Indicates whether the customer has children or not.               |
| `living_situation`            | Describes the living situation of the customer.                   |
| `total_experience`            | The total work experience of the customer in months.              |
| `income`                      | Customer's monthly income.                                        |
| `job_sector`                  | The sector of employment for the customer (e.g., public, private). |
| `DTI`                         | Debt-to-Income Ratio: a ratio that compares a customer's total debt to their annual income. |
| `APR`                         | Annual Percentage Rate: the annual rate charged for borrowing, including fees and additional costs. |
| `ccr_tot_mounth_amt`          | Centralized Credit Registry Total Monthly Amount: the total monthly amount due on credit reported to the centralized credit registry. |
| `ccr_payed_loan_tot_amt`      | Centralized Credit Registry Paid Loan Total Amount: the total amount paid towards loans as reported to the centralized credit registry. |
| `ccr_act_loan_tot_rest_amt`   | Centralized Credit Registry Active Loan Total Rest Amount: the remaining amount in active loans as reported to the centralized credit registry. |
| `loan_status`                 | The current status of the loan (1 - loan application was rejected, 0 - loan application was approved). |


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

Ensure you have Python 3.9.2 or later installed on your system. It's recommended to use a virtual environment to maintain dependencies.


## Installing

Clone the repository to your local machine:

```bash
git clone https://github.com/Omar-Karimov/Credit-Decision-Model-MLOps.git 
```

After cloning the repository, navigate to the src/prediction_model directory:

```bash
cd Credit-Decision-Model-MLOps/src
```

Set up a virtual environment:

For Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```

For macOS and Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Install the package:

To install it in editable or developer mode

```bash
pip install -e .
```

Normal installation

```bash
pip install .
```

Packaging for distribution:

Note: The step `python setup.py sdist bdist_wheel` is for packaging the project for distribution. It's useful if you're contributing to the project or need to generate a distributable format of the package. Most users simply looking to install and use the project can skip this step.


```bash
python setup.py sdist bdist_wheel
```


## Directory Structure

Below is the structure for the `src/` directory, which contains the main components of the Credit Decision Model package:

```bash
Credit-Decision-Model-MLOps/
└── src/
    ├── prediction_model/
    │   ├── config/
    │   │   ├── __init__.py
    │   │   └── config.py
    │   ├── datasets/
    │   │   ├── __init__.py
    │   │   ├── test.csv
    │   │   └── train.csv
    │   ├── processing/
    │   │   ├── __init__.py
    │   │   ├── data_handling.py
    │   │   └── preprocessing.py
    │   ├── trained_models/
    │   │   ├── __init__.py
    │   │   └── classification.pkl
    │   ├── __init__.py
    │   ├── pipeline.py
    │   ├── predict.py
    │   ├── training_pipeline.py
    │   └── VERSION
    ├── tests/
    │   ├── pytest.ini
    │   └── test_prediction.py
    ├── MANIFEST.in
    ├── README.md
    ├── requirements.txt
    └── setup.py
```

## Additional Resources

For insights into the initial stages of data analysis and model development, please explore the Jupyter notebooks located in the Notebooks/ directory at the root of this project. While the comprehensive training pipeline, featuring a variety of machine learning models and grid search for hyperparameter tuning, is implemented in the training_pipeline.py script, the notebooks offer foundational knowledge and a focused look at using logistic regression for loan approval prediction.

Included Notebooks:
- `EDA_Loan.ipynb`: This notebook presents an exploratory data analysis (EDA) on the loan dataset, providing visual and statistical insights into the features that influence loan approval decisions.
- `Loan_Experiment.ipynb`: The emphasis is on demonstrating the application of machine learning operations (MLOps) practices rather than comparing multiple models. For a more comprehensive exploration of model selection and optimization, the training_pipeline.py script extends beyond logistic regression.

Additionally, the Notebooks folder includes:
- `log_trained_model_v1.pkl` - A pickle file of the trained logistic regression model ready for making predictions.
- `test.csv` and `train.csv` - Sample datasets used within the notebooks for demonstrating the model training and evaluation process.


## Usage

Once you have installed the package, you can use it to train the model with your data, evaluate its performance, and use it to make predictions. Here's how you can perform each of these steps:

### Training the Model

To train the model with the training dataset, run:

```bash
python -m prediction_model.training_pipeline
```


### Making Predictions with Test Data

```python
from prediction_model.predict import generate_predictions
from prediction_model.processing.data_handling import load_dataset
from prediction_model.config import config

# Load the test dataset
test_data = load_dataset(config.TEST_FILE)

# Select the first row of the test dataset
test_sample = test_data.iloc[0:1].to_dict(orient="records")

# Generate a prediction
prediction = generate_predictions(test_sample)
print(prediction)
```


### Making Predictions with Custom Data

```python
from prediction_model.predict import generate_predictions

# Example of custom data
custom_data = {
  "rate": 22.0,
  "amount": 25000.0,
  "purpose": "Personal",
  "period": 48,
  "cus_age": 45,
  "gender": "Male",
  "education_level": "Educated",
  "marital_status": "Married",
  "has_children": "Yes",
  "living_situation": "Independent",
  "total_experience": 120,
  "income": 7500.0,
  "job_sector": "Private",
  "DTI": 32.5,
  "APR": 33.3,
  "ccr_tot_mounth_amt": 1500.0,
  "ccr_payed_loan_tot_amt": 20000.0,
  "ccr_act_loan_tot_rest_amt": 10000.0
}


# Generate a prediction for the custom data
custom_prediction = generate_predictions(custom_data)
print(custom_prediction)
```



