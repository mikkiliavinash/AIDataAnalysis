import streamlit as st
import plotly.express as px


print(__file__)


def generate_chart(result, chart_type):
    print("===== NEW CHART GENERATOR LOADED =====")
    
    if chart_type == "line":

        fig = px.line(
            result,
            x=result.columns[0],
            y=result.columns[1],
            height=350
        )

        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "bar":

        fig = px.bar(
            result,
            x=result.columns[0],
            y=result.columns[1],
            height=350
        )

        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "pie":
        print("USING PLOTLY PIE")

        fig = px.pie(
            result,
            names=result.columns[0],
            values=result.columns[1],
            height=350,
            width=450
        )

        st.plotly_chart(fig, use_container_width=False)