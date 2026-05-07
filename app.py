import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


st.set_page_config(
    page_title="InsightForge AI",
    page_icon="📊",
    layout="wide"
)


st.title("📊 InsightForge AI")
st.markdown("### Upload CSV Files & Generate Analytics")

st.sidebar.header("Upload CSV File")

uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV File",
    type=["csv"]
)


if uploaded_file is not None:

    # Read CSV File
    df = pd.read_csv(uploaded_file)

  
    st.subheader("📁 Dataset Preview")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader("📌 Dataset Information")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Rows",
        df.shape[0]
    )

    col2.metric(
        "Total Columns",
        df.shape[1]
    )

    col3.metric(
        "Missing Values",
        df.isnull().sum().sum()
    )

    
    st.sidebar.header("Filter Dataset")

    filter_column = st.sidebar.selectbox(
        "Select Column",
        df.columns
    )

    unique_values = df[filter_column].dropna().unique()

    selected_values = st.sidebar.multiselect(
        "Select Values",
        unique_values,
        default=unique_values
    )

    filtered_df = df[
        df[filter_column].isin(selected_values)
    ]

    
    st.subheader("🔍 Filtered Dataset")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

   
    st.subheader("📈 Interactive Charts")

    chart_type = st.selectbox(
        "Select Chart Type",
        [
            "Bar Chart",
            "Line Chart",
            "Pie Chart",
            "Histogram",
            "Scatter Plot"
        ]
    )

    
    all_columns = filtered_df.columns.tolist()

    numeric_columns = filtered_df.select_dtypes(
        include=np.number
    ).columns.tolist()

    # Select X-Axis
    x_axis = st.selectbox(
        "Select X-Axis",
        all_columns
    )

   
    if len(numeric_columns) > 0:

        y_axis = st.selectbox(
            "Select Y-Axis",
            numeric_columns
        )

        fig = None

      
        if chart_type == "Bar Chart":

            fig = px.bar(
                filtered_df,
                x=x_axis,
                y=y_axis,
                title="Bar Chart"
            )

        # -----------------------------
        # LINE CHART
        # -----------------------------
        elif chart_type == "Line Chart":

            fig = px.line(
                filtered_df,
                x=x_axis,
                y=y_axis,
                title="Line Chart"
            )

        elif chart_type == "Pie Chart":

            fig = px.pie(
                filtered_df,
                names=x_axis,
                values=y_axis,
                title="Pie Chart"
            )

       
        elif chart_type == "Histogram":

            fig = px.histogram(
                filtered_df,
                x=x_axis,
                title="Histogram"
            )

       
        elif chart_type == "Scatter Plot":

            fig = px.scatter(
                filtered_df,
                x=x_axis,
                y=y_axis,
                title="Scatter Plot"
            )

        # Show Chart
        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.warning(
            "No numeric columns available for chart generation."
        )

   
    st.subheader("📊 Summary Statistics")

    st.write(
        filtered_df.describe()
    )

  
    csv = filtered_df.to_csv(
        index=False
    )

    st.download_button(
        label="⬇ Download Filtered CSV",
        data=csv,
        file_name="filtered_data.csv",
        mime="text/csv"
    )


else:

    st.info(
        "👈 Please upload a CSV file to continue."
    )