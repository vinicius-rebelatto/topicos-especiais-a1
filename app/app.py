import streamlit as st
import pandas as pd
from analyses.correlations import generate_correlations
from analyses.visualizations import plot_graphs

st.title("📊 Análises Automáticas de Dataset")

uploaded_file = st.file_uploader("Envie sua base de dados (.csv)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Visualização inicial dos dados:")
    st.dataframe(df.head())

    # Correlações
    st.write("### 🔗 Correlações")
    corr = generate_correlations(df)
    st.dataframe(corr)

    # Gráficos
    st.write("### 📈 Visualizações")
    plot_graphs(df)
else:
    st.info("Por favor, envie um arquivo CSV para começar.")
