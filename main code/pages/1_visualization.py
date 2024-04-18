import psycopg2
import pandas as pd
import streamlit as st
import plotly.express as px
st.set_page_config(page_title="Crop Production Data Visualization", page_icon="📊", layout="wide")
st.subheader("Crop Production Data Visualization")

# Database credentials
host = 'flora.db.elephantsql.com'
port = '5432'
database = 'mpfihddn'
user = 'mpfihddn'
password = 'VBBvfE2xpJjn6x-DeQBvxycZGMGLo7Sj'

# Establish a connection
conn = psycopg2.connect(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password
)    

# Function to fetch data from the database
def fetch_data(query):
    with conn.cursor() as cursor:
        cursor.execute(query)
        col_names = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
    return pd.DataFrame(data, columns=col_names)


# Function to fetch and display data based on user selection
def generate_data(state, year, selected_districts, selected_seasons, selected_crops):
    with conn.cursor() as cursor:
        district_condition = f"AND district IN {tuple(selected_districts)}" if selected_districts and len(
            selected_districts) > 1 else f"AND district = '{selected_districts[0]}'" if selected_districts else ""
        season_condition = f"AND season IN {tuple(selected_seasons)}" if selected_seasons and len(
            selected_seasons) > 1 else f"AND season = '{selected_seasons[0]}'" if selected_seasons else ""
        crop_condition = f"AND crop IN {tuple(selected_crops)}" if selected_crops and len(
            selected_crops) > 1 else f"AND crop = '{selected_crops[0]}'" if selected_crops else ""
        query = f"SELECT * FROM CropData WHERE state = '{state}' AND year = '{year}' {district_condition} {season_condition} {crop_condition} ORDER BY district;"
        cursor.execute(query)
        col_names = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()

    if not data:
        st.write("No data found for the selected criteria.")
    else:
        return pd.DataFrame(data, columns=col_names)


# Fetching data for initial display
initial_query = 'SELECT * FROM CropData ORDER BY state;'
initial_data = fetch_data(initial_query)


# Dropdown to select year
selected_year = st.selectbox('Select Year:',
                             ['1997-98', '1998-99', '1999-00', '2000-01', '2001-02', '2002-03', '2003-04', '2004-05',
                              '2005-06',
                              '2006-07', '2007-08', '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14',
                              '2014-15',
                              '2015-16', '2016-17', '2017-18', '2018-19', '2019-20', '2020-21'])

# Dropdown to select state
selected_state = st.selectbox('Select State:', sorted(initial_data['state'].unique()))

# Multi-select for districts based on the selected state
selected_districts = []
if st.checkbox('Select Multiple Districts'):
    selected_districts = st.multiselect('Select District(s):', sorted(
        initial_data[initial_data['state'] == selected_state]['district'].unique()), default=None)
    if len(selected_districts) < 2:
        st.warning("Please select more than one district.")
else:
    selected_district = st.selectbox('Select District:',
                                     sorted(initial_data[initial_data['state'] == selected_state]['district'].unique()))
    selected_districts.append(selected_district)

# Multi-select for seasons
selected_seasons = []
if st.checkbox('Select Multiple Seasons'):
    selected_seasons = st.multiselect('Select Season(s):', sorted(initial_data['season'].unique()), default=None)
    if len(selected_seasons) < 2:
        st.warning("Please select more than one season.")
else:
    selected_season = st.selectbox('Select Season:', sorted(initial_data['season'].unique()))
    selected_seasons.append(selected_season)

# Multi-select for crops
selected_crops = []
if st.checkbox('Select Multiple Crops'):
    selected_crops = st.multiselect('Select Crop(s):', sorted(initial_data['crop'].unique()), default=None)
    if len(selected_crops) < 2:
        st.warning("Please select more than one crop.")
else:
    selected_crop = st.selectbox('Select Crop:', sorted(initial_data['crop'].unique()))
    selected_crops.append(selected_crop)

# Generate and display data based on user selection
data = generate_data(selected_state, selected_year, selected_districts, selected_seasons, selected_crops)


# Check if data is None before using it
if data is not None:
    # Dropdowns to select x-axis and y-axis
    selected_x_axis = st.selectbox('Select X-Axis:', ['district', 'crop', 'year', 'season'])
    selected_y_axis = st.selectbox('Select Y-Axis:', ['area', 'production', 'yield'])

    # Function to suggest the best chart type based on data and user selections
    def suggest_best_chart(data, x_axis, y_axis):
        # Get the data types of x and y axes
        x_dtype = data[x_axis].dtype
        y_dtype = data[y_axis].dtype

        # Check the number of unique values for x and y axes
        num_unique_x = data[x_axis].nunique()
        num_unique_y = data[y_axis].nunique()

        # Determine the best chart type based on data characteristics
        if x_dtype == 'object' and num_unique_x <= 10:  # Categorical x-axis with few unique values
            if y_dtype == 'object' or num_unique_y <= 10:  # Categorical y-axis with few unique values
                return 'Bar Chart'  # Bar chart is suitable for comparing categorical data
            else:
                return 'Pie Chart'  # Pie chart is suitable for visualizing categorical data distribution
        elif x_dtype == 'object' or y_dtype == 'object':  # One of the axes is categorical
            return 'Bar Chart'  # Bar chart can handle categorical axes effectively
        elif num_unique_x <= 10:  # Few unique values in x-axis
            return 'Bar Chart'  # Bar chart can effectively represent data with few categories
        elif num_unique_x > 10 and num_unique_y > 10:  # Both axes have many unique values
            return 'Scatter Plot'  # Scatter plot can visualize relationships between two continuous variables
        else:
            return 'Line Chart'  # Line chart is suitable for visualizing trends over a continuous variable


    # Generate and display data based on user selection
    data = generate_data(selected_state, selected_year, selected_districts, selected_seasons, selected_crops)

    # Suggest the best chart type based on the selected data and axes
    best_chart_type = suggest_best_chart(data, selected_x_axis, selected_y_axis)

    # Dropdown to select chart type
    selected_chart_type = st.selectbox('Select Chart Type:', ['Auto (Best Guess)', 'Line Chart', 'Bar Chart', 'Pie Chart', 'Column Chart', 'Scatter Plot', 'Area Chart'])

    # Button to regenerate the chart
    if st.button('Generate Chart'):
        if selected_chart_type == 'Auto (Best Guess)':
            selected_chart_type = best_chart_type  # Use the suggested best chart type
        
        # Generate the selected chart type only if data exists
        if data is not None and not data.empty:
            if selected_chart_type == 'Line Chart':
                fig = px.line(data, x=selected_x_axis, y=selected_y_axis, color='crop')
            elif selected_chart_type == 'Bar Chart':
                fig = px.bar(data, x=selected_x_axis, y=selected_y_axis, color='crop')
            elif selected_chart_type == 'Pie Chart':
                fig = px.pie(data, names='crop', values=selected_y_axis)
            elif selected_chart_type == 'Scatter Plot':
                fig = px.scatter(data, x=selected_x_axis, y=selected_y_axis, color='crop')
            elif selected_chart_type == 'Area Chart':
                fig = px.area(data, x=selected_x_axis, y=selected_y_axis, color='crop')
            
            # Format title
            title = f"{selected_y_axis.capitalize()} ({'Hectare' if selected_y_axis == 'area' else 'Tonnes'}) vs {selected_x_axis.capitalize()}"

            # Add selected parameters to title
            title += f" ({selected_year}, {selected_state})"
            if len(selected_districts) == 1:
                title += f", District: {selected_districts[0]}"
            elif len(selected_districts) > 1:
                title += f", Districts: {', '.join(selected_districts)}"
            if len(selected_seasons) == 1:
                title += f", Season: {selected_seasons[0]}"
            elif len(selected_seasons) > 1:
                title += f", Seasons: {', '.join(selected_seasons)}"
            
            # Update chart layout with title
            fig.update_layout(title=title)

            # Display the chart
            st.plotly_chart(fig)
        else:
            st.write("No data found for the selected criteria.")
