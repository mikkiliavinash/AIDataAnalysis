import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(layout="wide")

st.title("AI Assistent V1")

user_file = st.file_uploader("Choose File (CSV) or Excel only", type=["csv","xlsx"])

if user_file is not None:
    file_type = Path(user_file.name).suffix

    try:
        if file_type == ".xlsx":
            df = pd.read_excel(user_file)
        elif file_type ==".csv":
            df = pd.read_csv(user_file)
    except Exception as ee:
        st.exception(ee)
        st.stop()

    if df.empty:
        st.warning("File is Empty")
        st.stop()
    rows,colums_count = df.shape
    columns = df.columns.tolist()
    datatype = df.dtypes.reset_index()
    
    datatype.columns = ["Column", "Data Type"]
    st.write(f"File Name: {user_file.name}")
    st.write(f"Extension: {Path(user_file.name).suffix}")

    meta_col,datatype_col,preview_col=st.columns(3)
    with meta_col:
        st.header("Meta Data")
        col1_metric, col2_metric, col3_metric = st.columns(3)
        with col1_metric:
            col1_metric.metric("No of Rows",rows)
        with col2_metric:
            col2_metric.metric("No of Columns",colums_count)
        with col3_metric:
            with st.expander('Column Name:'):
                st.dataframe(columns)
    with datatype_col:
        st.header("Data Types")
        st.dataframe(datatype)
    with preview_col:
        st.header("Data Table")
        st.dataframe(df.head())