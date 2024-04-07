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
#st.write("(Write something to explain how to tune the features)")
st.markdown("* **Education**")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    kindergarten_impt = st.slider("Kindergarten", 0.0 , 1.0, value = 0.5)
with col2:
    primary_impt = st.slider("Primary School", 0.0 , 1.0, value = 0.5)
with col3:
    secondary_impt = st.slider("Secondary School", 0.0, 1.0, value = 0.5)

st.markdown("* **Property**")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    psf_pp_avg_impt = st.slider("Average PSF (Private Property)", 0.0 , 1.0, value = 0.5)
with col2:
    psf_hdb_avg_impt = st.slider("Average PSF (HDB)", 0.0, 1.0, value = 0.5)


st.markdown("* **Amenities**")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    gyms_impt = st.slider("Gyms", 0.0, 1.0, value = 0.5)
with col2:
    supermarkets_impt = st.slider("Supermarkets", 0.0, 1.0, value = 0.5)
with col3:
    hawkercentres_impt = st.slider("Hawker Centres", 0.0, 1.0, value = 0.5)
with col4:
    parks_impt = st.slider("Parks", 0.0, 1.0, value = 0.5)
with col5:
    pharmacies_impt = st.slider("Pharmacies", 0.0, 1.0, value = 0.5)


st.markdown("* **Transportation**")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    n_transport = st.slider("Transportation Availability", 0.0, 1.0, value = 0.5)

st.markdown("* **Population**")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    pop_denisty_impt = st.slider("Population Density (population per sq km)", 0.0, 1.0, value = 0.5)

## CHANGE THIS ##
# Finding the weighted avg
weights = np.array([kindergarten_impt, primary_impt, secondary_impt, psf_pp_avg_impt, psf_hdb_avg_impt, n_transport, gyms_impt, supermarkets_impt, hawkercentres_impt, parks_impt, pharmacies_impt, pop_denisty_impt]) # Order must be the same as the columns in the excel file
weights_str = ['Kindergarten', 'Primary', 'Secondary', 'Average PSF (Private)', 'Avergage PSF (HDB)', 'Transportation', 'Gym', 'Supermarket', 'Hawker Centres', 'Park', 'Pharmacy', 'Population Density'] # Order must be the same as weights above
score = (all_data.iloc[:,1:]  @ weights)/weights.sum(0)
all_data['total_score'] = score

#####################################################
radar_col, map_col = st.columns(2)
with radar_col:
    st.subheader("Radar Chart")
    radar_df = pd.DataFrame(dict(r = weights,
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


#####################################################
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

#####################################################
st.subheader("Top 5 Districts")
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

