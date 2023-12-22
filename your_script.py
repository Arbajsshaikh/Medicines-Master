import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Read data from Excel file
excel_file_path = 'PLOTTING_DATA_AVG_DIST_DISTRIBUTION.xlsx'  # Update with your actual file path
df = pd.read_excel(excel_file_path, index_col='Medicine Name', engine='openpyxl')

# Function for creating the bar plot
def MED_BAR_PLOT(dataframe, row_name):
    if row_name not in dataframe.index:
        st.warning(f"Row '{row_name}' not found in the dataframe.")
        return

    selected_row = dataframe.loc[row_name]
    selected_columns = selected_row[:-1]

    # Sort values in descending order
    sorted_values = selected_columns.sort_values(ascending=False)

    # Set a larger figure size for a more horizontal appearance
    fig, ax = plt.subplots(figsize=(28, 12))

    # Create a bar chart
    bars = ax.bar(sorted_values.index, sorted_values.values, label='Row Values')

    # Add value annotations on top of each bar with 90 degrees rotation
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.005, round(yval, 2), ha='center', va='bottom',
                rotation=90)

    # Add a horizontal line for 'avg_mean' in red
    avg_mean_value = selected_row['avg_mean']
    ax.axhline(y=avg_mean_value, color='red', linestyle='--', label='avg_mean')

    ax.set_xlabel('Column Names')
    ax.set_ylabel('Values')
    ax.set_title(f'Bar Chart for: {row_name}')

    # Rotate x-axis labels to 90 degrees
    ax.tick_params(axis='x', rotation=90)

    ax.legend()
    st.pyplot(fig)

# Unique values for row selection
unique_rows = df.index.unique()

# Create selector widget
row_selector = st.selectbox('Select Row:', ['Select Row'] + list(unique_rows))

# Display bar plot on row selection
if row_selector != 'Select Row':
    MED_BAR_PLOT(df, row_selector)
