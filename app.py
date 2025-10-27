import streamlit as st
import pandas as pd

st.title("🌾 Agriculture & Rainfall Q&A System")

# Upload data files
rainfall_file = st.file_uploader("Upload Rainfall Data (CSV)", type="csv")
crop_file = st.file_uploader("Upload Crop Production Data (CSV)", type="csv")

if rainfall_file and crop_file:
    rainfall_df = pd.read_csv(rainfall_file)
    crop_df = pd.read_csv(crop_file)

    st.subheader("Rainfall Data Preview")
    st.dataframe(rainfall_df.head())

    st.subheader("Crop Production Data Preview")
    st.dataframe(crop_df.head())

    # Example comparison: Average rainfall by state
    if "State" in rainfall_df.columns and "Rainfall" in rainfall_df.columns:
        avg_rainfall = rainfall_df.groupby("State")["Rainfall"].mean().reset_index()
        st.subheader("🌧️ Average Annual Rainfall by State")
        st.bar_chart(avg_rainfall.set_index("State"))

    # Example crop production chart
    if "Crop" in crop_df.columns and "Production" in crop_df.columns:
        top_crops = crop_df.groupby("Crop")["Production"].sum().nlargest(5).reset_index()
        st.subheader("🌾 Top 5 Most Produced Crops")
        st.bar_chart(top_crops.set_index("Crop"))
else:
    st.info("⬆️ Please upload both Rainfall and Crop Production CSV files to see results.")

