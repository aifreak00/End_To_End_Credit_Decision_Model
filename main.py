from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import numpy as np
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from prediction_model.predict import generate_predictions


app = FastAPI(
    title="Credit Decision Model API",
    description="A FastAPI application for automating credit decision evaluations. It utilizes a machine learning model to predict loan approval outcomes based on customer information.",
    version="1.0"
)


origins=[
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers= ["*"]
)

class LoanApplication(BaseModel):
    rate: float
    amount: float
    purpose: str
    period: int
    cus_age: int
    gender: str
    education_level: str
    marital_status: str
    has_children: str
    living_situation: str
    total_experience: int
    income: float
    job_sector: str
    DTI: float
    APR: float
    ccr_tot_mounth_amt: float
    ccr_payed_loan_tot_amt: float
    ccr_act_loan_tot_rest_amt: float



@app.get("/")
def index():
    return {"message": "Welcome to Credit Decision Model APP"}

@app.post("/prediction_api")
def predict_loan_approval(loan_details: LoanApplication):
    data = loan_details.dict()
    prediction = generate_predictions([data])["Predictions"][0]
    return {"Status": prediction}


@app.post("/prediction_ui")
def predict_loan_approval_form(
    rate: float,
    amount: float,
    purpose: str,
    period: int,
    cus_age: int,
    gender: str,
    education_level: str,
    marital_status: str,
    has_children: str,
    living_situation: str,
    total_experience: int,
    income: float,
    job_sector: str,
    DTI: float,
    APR: float,
    ccr_tot_mounth_amt: float,
    ccr_payed_loan_tot_amt: float,
    ccr_act_loan_tot_rest_amt: float):
    
    input_data = [rate, amount, purpose, period, cus_age,
                  gender, education_level, marital_status, has_children,
                  living_situation, total_experience, income,
                  job_sector, DTI, APR, ccr_tot_mounth_amt,
                  ccr_payed_loan_tot_amt, ccr_act_loan_tot_rest_amt]
    
    cols = ["rate", "amount", "purpose", "period", "cus_age",
            "gender", "education_level", "marital_status", "has_children",
            "living_situation", "total_experience", "income", "job_sector",
            "DTI", "APR", "ccr_tot_mounth_amt",
            "ccr_payed_loan_tot_amt", "ccr_act_loan_tot_rest_amt"]
    
    data_dict = dict(zip(cols, input_data))
    prediction = generate_predictions([data_dict])["Predictions"][0]
    return {"Status": prediction}


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)


    
