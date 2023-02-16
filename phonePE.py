# -*- coding: utf-8 -*-
import streamlit as st
import pymysql
import mysql.connector
import pandas as pd

@st.cache(allow_output_mutation=True)
def get_connection():
    return create_engine("mssql+pyodbc://root:sivasurya@localhost/agg_transacdata_india?driver=ODBC+Driver+17+for+SQL+Server", 
    fast_executemany = True
    )

conn = get_connection()

@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()



st.title("PhonePE")
tab1,tab2=st.tabs(["graph","Datas"])

with st.sidebar:
    st.title("Sidebar")




with tab1:
    st.header("plots")
    #mysql server connection
    
    databases=run_query("show databases;")
        
    tables=run_query("USE agg_transacdata_india")

    tables_list=run_query("show tables;")

    agg_2019_india=run_query("SELECT * FROM agg_2019_india")

    data=pd.read_sql("SELECT * FROM agg_2019_india",mydb)
    df1=pd.DataFrame(data)
    st.dataframe(data)

    import plotly.figure_factory as ff
    x=data["transaction_type"]
    y=data["tv_q1"]
    import plotly.express as px
    fig=px.bar(data,x,y)
    st.plotly_chart(fig)
  
with tab2:
    st.header("Transaction datas")
    option=st.selectbox("Select",("Q1 2019","Q2 2019","Q3 2019","Q4 2019"))
    if option=="Q1 2019":
        df2=df1[['transaction_type','tv_q1','tc_q1']]
        st.dataframe(df2,200,210)




