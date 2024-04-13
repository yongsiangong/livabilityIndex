import plotly.express as px
import pandas as pd
import numpy as np
import json
import streamlit as st
from sklearn.preprocessing import MinMaxScaler

# Set the page configurations
st.set_page_config(layout="wide", page_title="SG Lions",)

# Main titla
st.title("SG Lions Livability Index")
st.write("""The SG Lions team has developed this tool to calculate a livability index for Singapore's distinct districts, helping users choose ideal residential areas according to their needs. 
            The tool will allow users to prioritize factors such as school proximity, public transport accessibility, property prices, and facility access, addressing the limitations of existing livability indices by 
            incorporating specific urban characteristics of Singapore. This initiative aims to improve urban living and planning by facilitating informed residential choices.""")
# Read data
all_data = pd.read_excel("all_data.xlsx")
with open("district.json") as file:
    geojson_data = json.load(file) # geojson to create the amp
district_location_map_df = pd.read_excel('district_location_map.xlsx')
district_location_map_dict = dict(zip(district_location_map_df['district'], district_location_map_df['location']))# Get a district to location mapping


# MinMax transformation of the features
scaler = MinMaxScaler()
all_data.iloc[:,1:] = scaler.fit_transform(all_data.iloc[:,1:])

#####################################################
st.subheader("Feature Importance")
st.write("""To determine how livable different districts are, each district is scored using factors such as schools, property prices, transport, ammenities and population density. 
            \nEach factor has a value that has been adjusted to be comparable across all districts. 
            \nA user can assign importance to these factors by giving each a weight between 0 (not important) and 1 (very important). 
            \nThe livability score for each district is then calculated by taking an average of these weighted factors.""")
default = 0.0

if 'kindergarten_impt' not in st.session_state:
    st.session_state['kindergarten_impt'] = default
if 'primary_impt' not in st.session_state:
    st.session_state['primary_impt'] = default
if 'secondary_impt' not in st.session_state:
    st.session_state['secondary_impt'] = default
if 'psf_pp_avg_impt' not in st.session_state:
    st.session_state['psf_pp_avg_impt'] = default
if 'psf_hdb_avg_impt' not in st.session_state:
    st.session_state['psf_hdb_avg_impt'] = default
if 'gyms_impt' not in st.session_state:
    st.session_state['gyms_impt'] = default
if 'supermarkets_impt' not in st.session_state:
    st.session_state['supermarkets_impt'] = default
if 'hawkercentres_impt' not in st.session_state:
    st.session_state['hawkercentres_impt'] = default
if 'parks_impt' not in st.session_state:
    st.session_state['parks_impt'] = default
if 'pharmacies_impt' not in st.session_state:
    st.session_state['pharmacies_impt'] = default
if 'n_transport' not in st.session_state:
    st.session_state['n_transport'] = default
if 'pop_density_impt' not in st.session_state:
    st.session_state['pop_density_impt'] = default

if 'reset_flag' not in st.session_state:
    st.session_state['reset_flag'] = False

st.markdown("* **Education**")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    kindergarten_impt = st.slider(
        "Kindergarten", min_value = 0.0, max_value = 1.0,
        value = default if st.session_state['reset_flag'] else st.session_state['kindergarten_impt'],
        key = 'kindergarten_impt'
    )
with col2:
    primary_impt = st.slider(
        "Primary School", min_value = 0.0 , max_value = 1.0, 
        value = default if st.session_state['reset_flag'] else st.session_state['primary_impt'], 
        key = 'primary_impt')
with col3:
    secondary_impt = st.slider(
        "Secondary School", min_value = 0.0, max_value = 1.0, 
        value = default if st.session_state['reset_flag'] else st.session_state['secondary_impt'], 
        key = 'secondary_impt')

st.markdown("* **Property**")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    psf_pp_avg_impt = st.slider(
        "Average PSF (Private Property)", min_value = 0.0 , max_value = 1.0, 
        value = default if st.session_state['reset_flag'] else st.session_state['psf_pp_avg_impt'], 
        key = 'psf_pp_avg_impt')
with col2:
    psf_hdb_avg_impt = st.slider(
        "Average PSF (HDB)", min_value = 0.0, max_value = 1.0, 
        value = default if st.session_state['reset_flag'] else st.session_state['psf_hdb_avg_impt'], 
        key = 'psf_hdb_avg_impt')

st.markdown("* **Amenities**")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    gyms_impt = st.slider(
        "Gyms", min_value = 0.0, max_value = 1.0, 
        value = default if st.session_state['reset_flag'] else st.session_state['gyms_impt'], 
        key = 'gyms_impt')
with col2:
    supermarkets_impt = st.slider(
        "Supermarkets", min_value = 0.0, max_value = 1.0, 
        value = default if st.session_state['reset_flag'] else st.session_state['supermarkets_impt'], 
        key = 'supermarkets_impt')
with col3:
    hawkercentres_impt = st.slider(
        "Hawker Centres", min_value = 0.0, max_value = 1.0, 
        value = default if st.session_state['reset_flag'] else st.session_state['hawkercentres_impt'], 
        key = 'hawkercentres_impt')
with col4:
    parks_impt = st.slider(
        "Parks", min_value = 0.0, max_value = 1.0, 
        value = default if st.session_state['reset_flag'] else st.session_state['parks_impt'], 
        key = 'parks_impt')
with col5:
    pharmacies_impt = st.slider(
        "Pharmacies", min_value = 0.0, max_value = 1.0, 
        value = default if st.session_state['reset_flag'] else st.session_state['pharmacies_impt'], 
        key = 'pharmacies_impt')

st.markdown("* **Transportation**")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    n_transport = st.slider(
        "Transportation Availability", min_value = 0.0, max_value = 1.0, 
        value = default if st.session_state['reset_flag'] else st.session_state['n_transport'], 
        key = 'n_transport')

st.markdown("* **Population**")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    pop_density_impt = st.slider(
        "Population Density (population per sq km)", min_value = 0.0, max_value = 1.0, 
        value = default if st.session_state['reset_flag'] else st.session_state['pop_density_impt'], 
        key = 'pop_density_impt')

weights = np.array([kindergarten_impt, primary_impt, secondary_impt, 1-psf_pp_avg_impt, 1-psf_hdb_avg_impt, n_transport, gyms_impt, supermarkets_impt, hawkercentres_impt, parks_impt, pharmacies_impt, 1-pop_density_impt]) # Order must be the same as the columns in the excel file
weights_str = ['Kindergarten', 'Primary', 'Secondary', 'Average PSF (Private)', 'Avergage PSF (HDB)', 'Transportation', 'Gym', 'Supermarket', 'Hawker Centres', 'Park', 'Pharmacy', 'Population Density'] # Order must be the same as weights above
score = (all_data.iloc[:,1:]  @ weights)/weights.sum(0)
all_data['total_score'] = score

radar_col, map_col = st.columns(2)
with radar_col:
    st.subheader("Radar Chart")
    st.write("Summary of the feature importance")
    weights_radar = np.array([kindergarten_impt, primary_impt, secondary_impt, psf_pp_avg_impt, psf_hdb_avg_impt, n_transport, gyms_impt, supermarkets_impt, hawkercentres_impt, parks_impt, pharmacies_impt, pop_density_impt])
    radar_df = pd.DataFrame(dict(r = weights_radar,
                                 theta= weights_str
                                 )
                            )
    radar = px.line_polar(radar_df, r = 'r', theta = 'theta', line_close = True, template = 'ggplot2')

    radar.update_polars(angularaxis_showgrid = False,
                        radialaxis_gridwidth = 1,
                        gridshape = "linear",
                        radialaxis_showticklabels = True,
                        radialaxis_autorange= False,
                        radialaxis_color= 'black',
                        radialaxis_linecolor = 'black'
                        )
    radar.update_traces(fill = 'toself')
    radar.update_layout(height=600, width=700)
    st.plotly_chart(radar)

with map_col:
    st.subheader("Livability Index by District")
    #st.write("(Write something here?)")
    for feature in geojson_data["features"]:
        feature["properties"]["id"] = int(feature["properties"]["id"])
    geojson_df = pd.json_normalize(geojson_data["features"], sep="_")
    merged_data = pd.merge(geojson_df, all_data, left_on = "properties_id", right_on="district", how="left")
    fig1 = px.choropleth_mapbox(merged_data,
                               geojson = geojson_data,
                               locations = "properties_id",
                               color = "total_score",
                               color_continuous_scale = 'reds',
                               range_color = (merged_data["total_score"].min(), merged_data["total_score"].max()),
                               mapbox_style = "carto-positron",
                               zoom = 10,
                               center = {"lat": 1.3521, "lon": 103.8198}, # Centering on Singapore
                               opacity = 0.7,
                               labels = {"total_score": "Total Score"},
                               featureidkey = "properties.id",
                               hover_name = 'properties_name',
                               hover_data = {'total_score': True, 'properties_id': False}
                              )
    fig1.update_geos(fitbounds = "locations", visible=False)
    fig1.update_layout(height = 600, width = 800)



    st.plotly_chart(fig1)

st.subheader("Top 3 Districts")
st.write("""Here is your personalized score based on the importance you place on different features. This score is displayed on the map below, where varying shades of red indicate the level of livability — the darker the red, the higher the score.""")
top_3_df = all_data.sort_values('total_score', ascending = False).head(3)
top_3_df['location'] = top_3_df['district'].apply(lambda x: district_location_map_dict.get(x,x))

first, second, third = st.columns(3)
with first:
    st.markdown(f"""
                * **District {top_3_df['district'].values[0]}**\n
                Locations: {top_3_df['location'].values[0]}\n
                Total scores: {round(top_3_df['total_score'].values[0],3)}\n
                """)
with second:
    st.markdown(f"""
                * **District {top_3_df['district'].values[1]}**\n
                Locations: {top_3_df['location'].values[1]}\n
                Total scores: {round(top_3_df['total_score'].values[1],3)}\n
                """)
with third:
    st.markdown(f"""
                * **District {top_3_df['district'].values[2]}**\n
                Locations: {top_3_df['location'].values[2]}\n
                Total scores: {round(top_3_df['total_score'].values[2],3)}\n
                """)

# for troubleshooting
# st.write("Current session state before reset:", st.session_state)

def reset_values():
    st.session_state['reset_flag'] = not st.session_state['reset_flag']

if st.button('Reset'):
    reset_values()
    st.experimental_rerun()

if st.session_state['reset_flag'] is True:
    st.session_state['reset_flag'] = not st.session_state['reset_flag']
    st.experimental_rerun()
