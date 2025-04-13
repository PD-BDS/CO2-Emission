import streamlit as st
import pandas as pd
import requests
import plotly.express as px

API = "http://backend:8000"

st.title("🌍 CO₂ Emission Forecasting Dashboard")

tab1, tab2, tab3, tab4 = st.tabs(["Last 24h Emissions", "Next 6h Forecast", "Recent Predictions vs Actual", "Model Info"])

with tab1:
    r = requests.get(f"{API}/last-24h-emissions")
    df = pd.DataFrame(r.json())
    fig = px.line(df, x="TimeStamp", y="CO2Emission", title="Last 24 Hours CO₂ Emissions")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    r = requests.get(f"{API}/next-6h-predictions")
    df = pd.DataFrame(r.json())
    fig = px.line(df, x="TimeStamp", y="Prediction", title="Next 6 Hours Forecast")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    r = requests.get(f"{API}/last-6h-predictions-vs-actual")
    df = pd.DataFrame(r.json())
    fig = px.line(df.melt(id_vars="TimeStamp", value_vars=["Prediction", "Actual"]),
                  x="TimeStamp", y="value", color="variable", title="Prediction vs Actual (Last 6h)")
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    r = requests.get(f"{API}/latest-model")
    model = r.json()[0]
    st.metric("Model", model['Model_name'])
    st.metric("Version", model['Version'])
    st.metric("Pseudo Accuracy", f"{model['Pseudo_accuracy']:.2f}%")
    st.metric("RMSE", f"{model['RMSE']:.2f}")
    st.metric("MAE", f"{model['MAE']:.2f}")
    st.metric("R²", f"{model['R2']:.2f}")
