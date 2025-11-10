#app/analyses/vizualizations.py
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def plot_graphs(df):
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) >= 2:
        fig, ax = plt.subplots()
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)
