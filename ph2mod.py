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
conn = sqlite3.connect(r"\Users\THIS PC\OneDrive\Desktop\phonepe\db\phonepedb.db")


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
    
def generate_choropleth_map(data,quarter_map):
    # Load the GeoJSON data for India's states
    with open(r"\Users\THIS PC\Downloads\india_states.geojson.txt") as f:
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
        q1=f"""Select * from agg_{s_year}_india;"""
        df=pd.read_sql(q1, conn)

        # Create a pie chart using Plotly
        fig = go.Figure(data=[go.Pie(labels=df['Transaction_type'], values=df[f'Agg_count_{s_year}'])])
        fig.update_layout(title=str(s_year))

        # Display the chart in Streamlit
        st.plotly_chart(fig)

    else:
        quarter = st.selectbox("Select Quarter", ("Q1", "Q2", "Q3", "Q4"))
        # Show data for a specific year and quarter
        q1=f"""Select * from agg_{year}_india;"""
        df1=pd.read_sql(q1, conn)
        #df = eval(f"agg_data_{year}")
        if quarter == "Q1":
            show_dataframe(df1, "Q1")
            show_bar_chart(df1, "Q1")
        elif quarter == "Q2":
            show_dataframe(df1, "Q2")
            show_bar_chart(df1, "Q2")
        elif quarter == "Q3":
            show_dataframe(df1, "Q3")
            show_bar_chart(df1, "Q3")
        elif quarter == "Q4":
            show_dataframe(df1, "Q4")
            show_bar_chart(df1, "Q4")

# Define UI components for tab2 (not shown in this simplified version)
with tab2:
    st.header('Geo Data')
    year_m = st.radio("Select Year", (2018, 2019, 2020, 2021, 2022), horizontal=True)
    quarter_map = st.selectbox("Select Quarter", ("M1", "M2", "M3", "M4"))
    
    q2=f"""Select * from agg_{year_m}_map;"""
    df2=pd.read_sql(q2, conn)
    #df1 = eval(f"agg_{year_m}_map")
    generate_choropleth_map(df2, quarter_map)

 

        
            
            
        
    
    

