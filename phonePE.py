# -*- coding: utf-8 -*-
import streamlit as st
import pymysql
import mysql.connector
import pandas as pd
st.title("PhonePE")
tab1,tab2=st.tabs(["graph","Datas"])

with st.sidebar:
    st.title("Sidebar")




with tab1:
    st.header("plots")
    #mysql server connection
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="sivasurya",
      database="agg_transacdata_india"
    #auth_plugin='mysql_native_password'
    )
    def run_query(query):
        with mydb.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    databases=run_query("show databases;")
        
    tables=run_query("USE agg_transacdata_india")

    tables_list=run_query("show tables;")
    #for row in tables_list:
        #st.write(row)

    agg_2019_india=run_query("SELECT * FROM agg_2019_india")
    #for row in agg_2019_india:
        #st.write(row)

    x=run_query("SELECT tv_q1 FROM agg_2019_india")
    #st.write(x[0][0],x[1][0])


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




