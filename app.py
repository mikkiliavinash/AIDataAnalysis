import streamlit as st
from utils.loader import load_file
from utils.validator import validate_file
from utils.metadata import get_metadata
from llm.model import llm
from llm.prompts.analysis_prompt import analysis_prompt 
from data_analysis import analyzer
from llm.intent_classifier import classify_intent
from llm.prompts.explanation_prompt import explanation_prompt
from data_analysis.analyzer import execute_operation


st.set_page_config(layout="wide")

st.title("AI Assistent V1")

user_file = st.file_uploader("Choose File (CSV) or Excel only", type=["csv","xlsx"])

if user_file is not None:

    try:
        df,filetype,file_name = load_file(user_file)
        
        print(df.groupby("FLAG")["AMOUNT"].sum())

        print(df.groupby("FLAG").size())

        print(df["FLAG"].unique())

        print(df.dtypes)
        
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
                st.metric("File Type",filetype)

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

    st.session_state["df"] =df
    st.session_state["display_file_type"]=filetype
    st.session_state["file_name"]=file_name
    st.session_state["metadata"]=metadata

    st.divider()

    st.subheader("Ask Questions About Your Data")


    user_input = st.chat_input("Ask a question about your data...")

    if "messages" not in st.session_state:
        st.session_state.messages=[]

    for message  in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input:
        with st.chat_message(name="user"):
            st.markdown(user_input)
            st.session_state.messages.append({"role": "user", "content": user_input})

        meta_data = st.session_state["metadata"]

        user_intent = classify_intent(question=user_input, columns=metadata["column_names"] )

        result = execute_operation(df, user_intent)

        operation = user_intent.operation.lower()

        column = user_intent.column

        print(user_intent)

        prompt  = explanation_prompt.invoke(
                    {
                        "operation": operation,
                        "column": column,
                        "result":result,
                        "question" :user_input
                    }
                )
        import pandas as pd

        result = execute_operation(df, user_intent)

#        if isinstance(result, pd.DataFrame):
 #           st.dataframe(result)        
        
        response = llm.invoke(prompt)

        with st.chat_message(name="assistant"):
            st.markdown(response.content)
            st.session_state.messages.append({"role": "assistant", "content": response.content})