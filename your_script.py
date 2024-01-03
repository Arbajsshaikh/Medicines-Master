import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

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

# Function for displaying top 100 values
def top_100_values_sorted(dataframe, column_name):
    if column_name not in dataframe.columns:
        return f"Column '{column_name}' not found in the dataframe."

    # Get the specified column
    selected_column = dataframe[column_name]

    # Sort values in descending order and select the top 100
    top_100_values = selected_column.sort_values(ascending=True).head(100)

    return pd.DataFrame(top_100_values, columns=[column_name])

# Read data from Excel file
your_dataframe = pd.read_csv(r"PLOTTING_DATA_AVG_DIST_DISTRIBUTION.csv", index_col='Medicine Name')
df = your_dataframe.copy()

# Unique values for row selection
unique_rows = df.index.unique()

# Create selector widget
row_selector = st.selectbox('Select Row:', ['Select Row'] + list(unique_rows))

# Display bar plot on row selection
if row_selector != 'Select Row':
    MED_BAR_PLOT(df, row_selector)

# Read data from Excel file
excel_file_path = 'GENERIC_AVG_DIST_DISTRIBUTION.csv'  # Update with your actual file path
df = pd.read_csv(excel_file_path, index_col='Medicine Name')

# Streamlit App
st.title('Top 100 Values Selector')

# Selector for column
selected_column = st.selectbox('Select Column', df.columns[1:])

# Display top 100 values
if selected_column:
    result = top_100_values_sorted(df, selected_column)
    st.dataframe(result)

# Assuming your data is stored in the 'filtered_data' DataFrame
filtered_data = pd.read_csv('DIST_Franchise-Orders-2022-23.csv')

# Create a dropdown widget for selecting a District
district_dropdown = st.selectbox('Select District:', filtered_data['DISTRICT'].unique())

# Create a function to update the Shop-Code options based on the selected District
def update_shop_code_options(selected_district):
    shop_code_options = filtered_data[filtered_data['DISTRICT'] == selected_district]['Shop-Code'].unique()
    return ['All'] + list(shop_code_options)

# Create a dropdown widget for selecting a Shop-Code
shop_code_dropdown = st.selectbox('Select Shop-Code:', update_shop_code_options(district_dropdown))

# Option to update Shop-Code options based on selected District
if st.button('Update Shop-Code Options'):
    shop_code_dropdown.options = update_shop_code_options(district_dropdown)

# Display the Medicine Names and Quantities based on the selected Shop-Code
if shop_code_dropdown != 'All':
    selected_data = filtered_data[(filtered_data['DISTRICT'] == district_dropdown) & (filtered_data['Shop-Code'] == shop_code_dropdown)]
else:
    selected_data = filtered_data[filtered_data['DISTRICT'] == district_dropdown]

# Sort the data by Qty in descending order
selected_data = selected_data.sort_values(by='Qty', ascending=False)

# Display the data
st.table(selected_data[['Medicine Name', 'Qty']])

# Display a bar plot using Plotly Express
if st.checkbox('Show Bar Plot'):
    fig = px.bar(
        selected_data,
        x='Medicine Name',
        y='Qty',
        title=f'Medicine Qty in {district_dropdown}, Shop-Code: {shop_code_dropdown}',
        labels={'Qty': 'Quantity'},
    )
    st.plotly_chart(fig)
