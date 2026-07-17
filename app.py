import streamlit as st
from utils.loader import load_file
from utils.validator import validate_file
from utils.metadata import get_metadata
from llm.model import llm
from llm.intent_classifier import classify_intent
from llm.prompts.explanation_prompt import explanation_prompt
from data_analysis.analyzer import execute_operation
from visualization.chart_selector import select_chart
from visualization.chart_generator import generate_chart
print(generate_chart.__module__)
print(generate_chart.__code__.co_filename)
import pandas as pd
from utils.metadata_formatter import format_metadata
from llm.schemas import Intent


st.set_page_config(layout="wide")

st.title("AI Assistent V1")

user_file = st.file_uploader("Choose File (CSV) or Excel only", type=["csv","xlsx"])
print("File Upladed")

if user_file is not None:
    try:
        df,filetype,file_name = load_file(user_file)
        print("File Loaded")
    except Exception as e:
         st.exception(e)
         st.stop()
    try:
         validate_file(df)
         print("File Validated")
    except ValueError as e:
         st.error(str(e))
         st.stop()

    metadata =get_metadata(df)
    print("Meta Data Created")

    formatted_metadata = format_metadata(metadata)

    print("Meta Data Formated")

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
    st.session_state["formatted_metadata"] = formatted_metadata


    st.divider()
    st.subheader("Ask Questions About Your Data")
    user_input = st.chat_input("Ask a question about your data...")



    if "messages" not in st.session_state:
        st.session_state.messages=[]
        print("Chat Started")

    for message  in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input:
        print("User Intent Given")
        with st.chat_message(name="user"):
            st.markdown(user_input)
            st.session_state.messages.append({"role": "user", "content": user_input})
        meta_data = st.session_state["metadata"]

        user_intent = classify_intent(question=user_input,metadata=formatted_metadata)
        print(user_intent)
        print(user_intent.model_dump())

        
        if user_intent.operation is None:
            st.error("AI couldn't determine the operation.")
            st.stop()

        if (
            user_intent.columns is None
            and user_intent.operation.lower() != "count"
        ):
            st.error("AI couldn't determine the target column.")
            st.stop()

        result = execute_operation(df, user_intent)
            
        operation = user_intent.operation.lower()

        column = user_intent.columns
        
        prompt  = explanation_prompt.invoke(
                    {
                        "operation": operation,
                        "columns": column,
                        "result":result,
                        "question" :user_input
                    }
                )

        with st.chat_message("assistant"):
            if user_intent.visualization and user_intent.operation is None:
                chart_type = user_intent.visualization_type
                print("********************-Chart_Generation Group BY ********************")
                if user_intent.group_by:
                    user_intent.operation = "SUM"
                generate_chart(result, chart_type)

            if (user_intent.visualization and isinstance(result, pd.DataFrame) and not result.empty and result.shape[1] >= 2 
                and result.shape[0] > 1):
                print("********************-Chart_Generation ********************")
                chart_type = user_intent.visualization_type
                generate_chart(result, chart_type)
    

            if isinstance(result, pd.DataFrame):
                if result.shape == (1, 1):
                    st.metric(
                        label=result.columns[0],
                        value=result.iloc[0, 0]
                    )

                else:
                    st.dataframe(result, hide_index=True)
            elif isinstance(result, pd.Series):
                st.dataframe(result.reset_index(), hide_index=True)
            else:
                st.metric("Result", result)

            response = llm.invoke(prompt)

            st.markdown(response.content)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response.content
            }
        )