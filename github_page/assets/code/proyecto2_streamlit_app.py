import streamlit as st
import pandas as pd
import plotly.express as px

car_data = pd.read_csv("vehicles_us.csv")

st.header("Analisis de anuncios de venta de vehiculos en EE. UU.")
st.write("Explora la distribucion de kilometraje y la relacion entre kilometraje y precio.")

hist_button = st.button("Construir histograma de odometro")
if hist_button:
    fig_hist = px.histogram(car_data, x="odometer", nbins=30)
    st.plotly_chart(fig_hist, use_container_width=True)

scatter_button = st.button("Construir grafico de dispersion precio vs odometro")
if scatter_button:
    fig_scatter = px.scatter(car_data, x="odometer", y="price", opacity=0.5)
    st.plotly_chart(fig_scatter, use_container_width=True)
