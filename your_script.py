# streamlit_app.py

import streamlit as st
import pandas as pd

def top_100_values_sorted(dataframe, column_name):
    if column_name not in dataframe.columns:
        return f"Column '{column_name}' not found in the dataframe."

    # Get the specified column
    selected_column = dataframe[column_name]

    # Sort values in descending order and select the top 100
    top_100_values = selected_column.sort_values(ascending=True).head(100)

    return pd.DataFrame(top_100_values, columns=[column_name])

# Read data from Excel file
excel_file_path = 'GENERIC_AVG_DIST_DISTRIBUTION.xlsx'  # Update with your actual file path
df = pd.read_excel(excel_file_path, index_col='Medicine Name', engine='openpyxl')
# Streamlit App
st.title('Top 100 Values Selector')

# Selector for column
selected_column = st.selectbox('Select Column', df.columns[1:])

# Display top 100 values
if selected_column:
    result = top_100_values_sorted(df, selected_column)
    st.dataframe(result)
