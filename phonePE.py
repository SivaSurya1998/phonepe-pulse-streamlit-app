# -*- coding: utf-8 -*-
import streamlit as st
import sqlite3
from sqlalchemy import create_engine
import pymysql
import mysql.connector
import pandas as pd
st.title("PhonePE")
tab1,tab2=st.tabs(["graph","Datas"])


conn=sqlite3.connect(phonepe.db)
print('Connection good')
cursor=conn.execute("""Select * from agg_2019_india;""")
data=pd.read_sql("""Select * from agg_2019_india;""",conn)
print("query done")



with tab1:
    st.header("plots")


    import plotly.figure_factory as ff
    x=data["Transaction type"]
    y=data["Total value_Q1"]
    import plotly.express as px
    fig=px.bar(data,x,y)
    st.plotly_chart(fig)

    
with tab2:
    st.header("Transaction datas")
    option=st.selectbox("Select",("Q1 2019","Q2 2019","Q3 2019","Q4 2019"))
    if option=="Q1 2019":
        df1=data[['Transaction type','Total value_Q1','Total_count_Q1']]
        st.dataframe(df1)




