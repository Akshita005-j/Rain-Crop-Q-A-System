import streamlit as st
import pandas as pd

st.set_page_config(page_title="Agriculture & Rainfall Q&A", page_icon="🌾", layout="wide")
st.title("🌾 Agriculture & Rainfall Q&A System")
st.markdown("Explore rainfall and crop production insights across Indian states.")

# ── Load built-in sample data ──
@st.cache_data
def load_default_data():
    crop = pd.DataFrame({
        "State": ["Rajasthan","Rajasthan","Rajasthan","Maharashtra","Maharashtra","Maharashtra","Punjab","Punjab","Punjab"],
        "Crop":  ["Wheat","Bajra","Maize","Sugarcane","Rice","Cotton","Rice","Wheat","Maize"],
        "Year":  [2020,2021,2022,2020,2021,2022,2020,2021,2022],
        "Production": [400,500,420,800,600,700,900,850,780]
    })
    rain = pd.DataFrame({
        "State": ["Rajasthan","Rajasthan","Rajasthan","Maharashtra","Maharashtra","Maharashtra","Punjab","Punjab","Punjab"],
        "Year":  [2020,2021,2022,2020,2021,2022,2020,2021,2022],
        "Rainfall": [312,298,350,450,430,480,520,505,560]
    })
    return crop, rain

st.sidebar.header("📂 Data Source")
use_upload = st.sidebar.radio("Choose data source:", ["Use sample data", "Upload my own CSVs"])

if use_upload == "Upload my own CSVs":
    rainfall_file = st.sidebar.file_uploader("Rainfall CSV", type="csv")
    crop_file = st.sidebar.file_uploader("Crop Production CSV", type="csv")
    if rainfall_file and crop_file:
        rain_df = pd.read_csv(rainfall_file)
        crop_df = pd.read_csv(crop_file)
        rain_df.columns = rain_df.columns.str.strip()
        crop_df.columns = crop_df.columns.str.strip()
    else:
        st.info("⬆️ Please upload both CSV files in the sidebar.")
        st.stop()
else:
    crop_df, rain_df = load_default_data()
    st.sidebar.success("✅ Using built-in sample data")

# ── RAINFALL SECTION ──
st.subheader("🌧️ Average Annual Rainfall by State")
avg_rain = rain_df.groupby("State")["Rainfall"].mean().reset_index()
avg_rain.columns = ["State", "Avg Rainfall (mm)"]
avg_rain = avg_rain.sort_values("Avg Rainfall (mm)", ascending=False)

col1, col2 = st.columns([2,1])
with col1:
    st.bar_chart(avg_rain.set_index("State"))
with col2:
    st.dataframe(avg_rain.reset_index(drop=True))

# ── RAINFALL Q&A ──
st.markdown("### ❓ Compare Rainfall Between States")
col1, col2 = st.columns(2)
states = sorted(rain_df["State"].unique())
with col1:
    s1 = st.selectbox("State 1", states, index=0)
with col2:
    s2 = st.selectbox("State 2", states, index=2)

if s1 and s2:
    avg = rain_df.groupby("State")["Rainfall"].mean()
    col1, col2 = st.columns(2)
    with col1:
        st.metric(f"☔ {s1} Avg Rainfall", f"{avg[s1]:.1f} mm")
    with col2:
        st.metric(f"☔ {s2} Avg Rainfall", f"{avg[s2]:.1f} mm",
                  delta=f"{avg[s2]-avg[s1]:.1f} mm vs {s1}")

st.markdown("---")

# ── CROP SECTION ──
st.subheader("🌾 Top Crops by Total Production")
top_crops = crop_df.groupby("Crop")["Production"].sum().nlargest(10).reset_index()
top_crops.columns = ["Crop", "Total Production"]

col1, col2 = st.columns([2,1])
with col1:
    st.bar_chart(top_crops.set_index("Crop"))
with col2:
    st.dataframe(top_crops.reset_index(drop=True))

# ── CROP Q&A ──
st.markdown("### ❓ Top Crops by State")
selected_state = st.selectbox("Select a state:", sorted(crop_df["State"].unique()))
if selected_state:
    state_crops = crop_df[crop_df["State"] == selected_state].groupby("Crop")["Production"].sum().sort_values(ascending=False).reset_index()
    state_crops.columns = ["Crop", "Production"]
    st.markdown(f"**Top crops in {selected_state}:**")
    col1, col2 = st.columns([1,2])
    with col1:
        st.dataframe(state_crops.reset_index(drop=True))
    with col2:
        st.bar_chart(state_crops.set_index("Crop"))

st.caption("Data source: Sample data based on data.gov.in (Crop Production & IMD Rainfall)")
