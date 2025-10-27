import pandas as pd

# Load data (you’ll replace filenames with your actual CSVs)
crop = pd.read_csv("crop_production.csv")
rain = pd.read_csv("rainfall_data.csv")

# Example: Compare rainfall in two states
def compare_rainfall(state1, state2, years=5):
    latest_year = rain['YEAR'].max()
    recent = rain[rain['YEAR'] >= latest_year - years + 1]
    avg = recent.groupby('STATE')['ANNUAL_RAINFALL'].mean()
    print(f"Average Rainfall ({years} years):")
    print(f"{state1}: {avg[state1]:.2f} mm")
    print(f"{state2}: {avg[state2]:.2f} mm")

# Example: Top crops in each state
def top_crops(state, top_n=3):
    state_data = crop[crop['STATE'] == state]
    latest_year = state_data['YEAR'].max()
    latest = state_data[state_data['YEAR'] == latest_year]
    top = latest.groupby('CROP')['PRODUCTION'].sum().sort_values(ascending=False).head(top_n)
    print(f"\nTop {top_n} crops in {state} ({latest_year}):")
    print(top)

# Example run
compare_rainfall("Rajasthan", "Punjab", 5)
top_crops("Rajasthan")
top_crops("Punjab")

print("\nSources: data.gov.in (Crop Production, IMD Rainfall Data)")
