import streamlit as st
import pandas as pd
import joblib

from simulator import simulator_page
from agent import customer_agent_page
from dashboard import dashboard_page
from report import report_page

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Customer Churn Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

# ---------- LOAD MODEL ----------
@st.cache_resource
def load_model():
    model = joblib.load("churn_model.pkl")
    features = joblib.load("features.pkl")
    return model, features

model, features = load_model()

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
    return df

df = load_data()

# ---------- IMPORT PAGES ----------
# (We will create these files next.)
from dashboard import dashboard_page
from agent import customer_agent_page
from simulator import simulator_page
from report import report_page

# ---------- SIDEBAR ----------
st.sidebar.title("📊 Customer Churn AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Customer Risk Agent",
        "What-If Simulator",
        "Reports",
        "About"
    ]
)

st.sidebar.markdown("---")

st.sidebar.success("Logistic Regression Model")

st.sidebar.write("Features:", len(features))
st.sidebar.write("Dataset Size:", len(df))

# ---------- PAGE ROUTER ----------
if page == "Dashboard":

    dashboard_page(
        df,
        model,
        features
    )

elif page == "Customer Risk Agent":

    customer_agent_page(
        model,
        features
    )

elif page == "What-If Simulator":

    simulator_page(
        model,
        features
    )

elif page == "Reports":

    report_page(
        df,
        model,
        features
    )

else:

    st.title("About This Project")

    st.markdown("""
# Customer Churn Intelligence Platform

This application helps managers identify customers at risk of leaving.

### Features

- Executive Dashboard
- Customer Churn Prediction
- AI Explanation
- Retention Recommendations
- Customer Risk Segmentation
- Revenue at Risk
- What-If Simulator
- Automatic Manager Report

### Machine Learning Model

- Logistic Regression

### Dataset

Telco Customer Churn Dataset
""")