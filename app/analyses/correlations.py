import pandas as pd

def generate_correlations(df: pd.DataFrame):
    numeric_df = df.select_dtypes(include=['number'])
    return numeric_df.corr().round(2)
