import streamlit as st
from utils.loader import load_file
from utils.validator import validate_file
from utils.metadat import get_metadata
st.set_page_config(layout="wide")

st.title("AI Assistent V1")

user_file = st.file_uploader("Choose File (CSV) or Excel only", type=["csv","xlsx"])

if user_file is not None:
    try:
        df,display_file_type,file_name = load_file(user_file)
    except Exception as e:
         st.exception(e)
         st.stop()

    try:
         validate_file(df)
    except ValueError as e:
         st.error(str(e))
         st.stop()

    metadata =get_metadata(df)

    tab1, tab2, tab3 = st.tabs(["Overview","Preview","Data Quality"])

    #Overview
    with tab1:
         metadata_container = st.container(horizontal=True)
         with metadata_container:
                #File Name
                st.metric("File Name",file_name)

                #File Type
                st.metric("File Type",display_file_type)

                #Total Rows
                st.metric("Total Rows", metadata["rows"])

                #Total Columns
                st.metric("Total Columns", metadata["column_count"])

                #Column Names
                with st.expander("Column Names"):
                    st.dataframe(metadata["column_names"], hide_index=True)

    #Preview
    with tab2:         

        preview_container = st.container(horizontal=True)

        with preview_container:
              #Data Types
              st.dataframe(metadata["data_types"], hide_index=True)
              #Data Frame First 100
              st.subheader("First 100 Rows")
              st.dataframe(df.head(100), hide_index=True)

    #Data Quality
    with tab3:
        quality_container = st.container(horizontal=True)

        with quality_container:

            missing_col1, missing_col2 = st.columns(2)

            with missing_col1:

                kpi_cal1,kpi_cal2 =st.columns(2)

                #Empty Rows Count
                with kpi_cal1:
                    st.metric("Total Empty Rows",metadata["num_empty_rows"])

                #Duplicates Count
                with kpi_cal2:
                     st.metric("Total Duplicates",metadata["total_duplicates"])

                #Empty Rows
                st.write("Empty Rows")
                if metadata["num_empty_rows"] > 0:
                    st.dataframe(metadata["empty_rows"], hide_index=True)
                else:
                    st.success("No empty rows found.")                

                #Duplicates Rows
                st.write("Duplicates")
                if metadata["total_duplicates"] > 0:
                    st.dataframe(metadata["duplicate_rows"], hide_index=True)
                else:
                    st.success("No Duplicate rows found.")

            #Missing Cells
            with missing_col2:
                 st.metric("Total Missing Cells",metadata["missing_count"])

                 #Missing Cells Rows
                 st.dataframe(metadata["missing_summary"], hide_index=True)

        memory_container  = st.container(horizontal=True)
        with memory_container:
             st.metric("Memory Use",metadata["memory_usage"])
