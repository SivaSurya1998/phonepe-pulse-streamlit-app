# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 00:16:25 2023

@author: THIS PC
"""

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import json
import plotly.graph_objects as go

# Connect to database
conn = sqlite3.connect(r"phonepedb.db")

# Read data from database tables
agg_data_2018 = pd.read_sql("""Select * from agg_2018_india;""", conn)
agg_data_2019 = pd.read_sql("""Select * from agg_2019_india;""", conn)
agg_data_2020 = pd.read_sql("""Select * from agg_2020_india;""", conn)
agg_data_2021 = pd.read_sql("""Select * from agg_2021_india;""", conn)
agg_data_2022 = pd.read_sql("""Select * from agg_2022_india;""", conn)

agg_2018_map=pd.read_sql("""Select * from agg_2018_map;""", conn)
agg_2019_map=pd.read_sql("""Select * from agg_2019_map;""", conn)
agg_2020_map=pd.read_sql("""Select * from agg_2020_map;""", conn)
agg_2021_map=pd.read_sql("""Select * from agg_2021_map;""", conn)
agg_2022_map=pd.read_sql("""Select * from agg_2022_map;""", conn)

# Define UI using Streamlit
st.title("PhonePE")
tab1, tab2 = st.tabs(["Datas","Map"])

# Define functions for visualizations
def show_bar_chart(df, quarter):
    x = df["Transaction_type"]
    y = df[f"Total_value_{quarter}"]
    fig = px.bar(df, x, y)
    st.plotly_chart(fig)

def show_dataframe(df, quarter):
    df = df[[f"Transaction_type", f"Total_value_{quarter}", f"Total_count_{quarter}"]]
    st.dataframe(df)
    
def generate_choropleth_map(data):
    # Load the GeoJSON data for India's states
    with open('india_states.geojson.txt') as f:
        india_states = json.load(f)

    # Create the choropleth map
    fig = px.choropleth(
        data,
        geojson=india_states,
        featureidkey='properties.ST_NM',
        locations='name',
        color=f'count_{quarter_map}',
        color_continuous_scale='Reds'
    )

    # Update the map layout
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
    title=dict(
        text="Total Transaction in Different quarters of  a year in each state",
        xanchor='center',
        x=0.5,
        yref='paper',
        yanchor='bottom',
        y=1,
        pad={'b': 10}
    ),
    margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
    height=300,
    width=200
    )
    # Display the map in Streamlit
    st.plotly_chart(fig, use_container_width=True)

# Define UI components for tab1
with tab1:
    st.header("Transaction datas")
    year = st.radio("Select Year", (2018, 2019, 2020, 2021, 2022, "Aggregated"), horizontal=True)
    

    if year == "Aggregated":
        # Select the year
        s_year = st.selectbox("Select Year", (2018, 2019, 2020, 2021, 2022))

        # Create a dictionary of the agg_data dataframes with their respective years as keys
        agg_data_dict = {
            2018: agg_data_2018,
            2019: agg_data_2019,
            2020: agg_data_2020,
            2021: agg_data_2021,
            2022: agg_data_2022
            }

        # Get the selected year's dataframe from the dictionary
        df = agg_data_dict[s_year]

        # Create a pie chart using Plotly
        fig = go.Figure(data=[go.Pie(labels=df['Transaction_type'], values=df[f'Agg_count_{s_year}'])])
        fig.update_layout(title=str(s_year))

        # Display the chart in Streamlit
        st.plotly_chart(fig)
    else:
        quarter = st.selectbox("Select Quarter", ("Q1", "Q2", "Q3", "Q4"))
        # Show data for a specific year and quarter
        df = eval(f"agg_data_{year}")
        if quarter == "Q1":
            show_dataframe(df, "Q1")
            show_bar_chart(df, "Q1")
        elif quarter == "Q2":
            show_dataframe(df, "Q2")
            show_bar_chart(df, "Q2")
        elif quarter == "Q3":
            show_dataframe(df, "Q3")
            show_bar_chart(df, "Q3")
        elif quarter == "Q4":
            show_dataframe(df, "Q4")
            show_bar_chart(df, "Q4")

# Define UI components for tab2 (not shown in this simplified version)
with tab2:
    st.header('Geo Data')
    year = st.radio("Select Year", (2018, 2019, 2020, 2021, 2022), horizontal=True)
    quarter_map= st.selectbox("Select Quarter", ("M1", "M2", "M3", "M4"))
    
    df = eval(f"agg_{year}_map")
    if quarter_map=='M1':
        generate_choropleth_map(df)
    elif quarter_map=='M2':
        generate_choropleth_map(df)
    elif quarter_map=='M3':
        generate_choropleth_map(df)
    elif quarter_map=='M4':
        generate_choropleth_map(df)   

        
            
            
        
    
    

