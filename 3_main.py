# Import necessary Streamlit libraries
import psycopg2
import pandas as pd
import streamlit as st
import base64
st.set_page_config(page_title="Crop Production Data Download", page_icon="📩", layout="wide")
st.markdown(
    f"""
    <style>
        .sidebar .sidebar-content {{
            background-image: url('https://images.app.goo.gl/t3vtFcmtgAUGKeWD6');
            background-repeat: no-repeat;
            background-position: center;
            background-size: cover;
            padding-top: 80px;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)



st.subheader("Crop Production Data Download")
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


# Fetching data for initial display
initial_query = 'SELECT * FROM CropData ORDER BY state;'
initial_data = fetch_data(initial_query)


# Function to fetch and display data based on user selection
def generate_data(state, year, selected_districts, selected_seasons, selected_crops):
    district_condition = f"AND district IN {tuple(selected_districts)}" if selected_districts and len(
        selected_districts) > 1 else f"AND district = '{selected_districts[0]}'" if selected_districts else ""
    season_condition = f"AND season IN {tuple(selected_seasons)}" if selected_seasons and len(
        selected_seasons) > 1 else f"AND season = '{selected_seasons[0]}'" if selected_seasons else ""
    crop_condition = f"AND crop IN {tuple(selected_crops)}" if selected_crops and len(
        selected_crops) > 1 else f"AND crop = '{selected_crops[0]}'" if selected_crops else ""
    query = f"SELECT * FROM CropData WHERE state = '{state}' AND year = '{year}' {district_condition} {season_condition} {crop_condition} ORDER BY district;"
    data = fetch_data(query)

    if data.empty:
        st.write("No data found for the selected criteria.")
    else:
        subheader_text = f"### Data for Year {year}:"
        subheader_text1 = f"\n**Selected Districts:** {selected_districts}"
        subheader_text2 = f"\n**Selected Seasons:** {selected_seasons}"
        subheader_text3 = f"\n**Selected Crops:** {selected_crops}"
        st.markdown(subheader_text)
        st.markdown(subheader_text1)
        st.markdown(subheader_text2)
        st.markdown(subheader_text3)
        st.write(data)


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

# Button to generate data
if st.button('Generate Data'):
    generate_data(selected_state, selected_year, selected_districts, selected_seasons, selected_crops)


def dwon_data(state, year, selected_districts, selected_seasons, selected_crops):
    district_condition = f"AND district IN {tuple(selected_districts)}" if selected_districts and len(
        selected_districts) > 1 else f"AND district = '{selected_districts[0]}'" if selected_districts else ""
    season_condition = f"AND season IN {tuple(selected_seasons)}" if selected_seasons and len(
        selected_seasons) > 1 else f"AND season = '{selected_seasons[0]}'" if selected_seasons else ""
    crop_condition = f"AND crop IN {tuple(selected_crops)}" if selected_crops and len(
        selected_crops) > 1 else f"AND crop = '{selected_crops[0]}'" if selected_crops else ""
    query = f"SELECT * FROM CropData WHERE state = '{state}' AND year = '{year}' {district_condition} {season_condition} {crop_condition} ORDER BY district;"
    data = fetch_data(query)
    return data


df = dwon_data(selected_state, selected_year, selected_districts, selected_seasons, selected_crops)


# def convert_df_to_downloadable(df, filename, format):
#     if format == 'CSV':
#         # Convert DataFrame to CSV string
#         csv = df.to_csv(index=False)
#         # Encode CSV string to base64
#         b64 = base64.b64encode(csv.encode()).decode()
#         # Create href link with base64 encoded CSV
#         href = f'<a href="data:text/csv;base64,{b64}" download="{filename}.csv">Download CSV</a>'
#     return href


# Streamlit app
st.title('Download Data')

# Download buttons
download_format = st.selectbox('Select download format:', ['CSV', ])

if st.button('Download'):
    download_link = convert_df_to_downloadable(df, 'data', download_format)
    st.markdown(download_link, unsafe_allow_html=True)




