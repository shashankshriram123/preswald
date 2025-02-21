import json
import pandas as pd
import matplotlib.pyplot as plt
import calmap
from datetime import datetime, timedelta

# Load JSON data
json_file = "/Users/shashankshriram/Downloads/preswald/examples/chess/fabianocaruanaAggregatedData.json"
with open(json_file, "r") as file:
    chess_data = json.load(file)

# Convert JSON into DataFrame
df = pd.DataFrame(chess_data)

# Ensure 'date' column is in datetime format
df["date"] = pd.to_datetime(df["date"])

# Define time range: Last 12 months from today
end_date = datetime.today().date()
start_date = (end_date - timedelta(days=365))  # Start exactly 1 year ago

print(f"📆 Start Date: {start_date}, End Date: {end_date}")

# Filter data for the last 12 months
df_filtered = df[(df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)].copy()

# Ensure all 365 days are present
all_dates = pd.date_range(start=start_date, end=end_date, freq="D")
df_filtered = df_filtered.set_index("date").reindex(all_dates, fill_value=0)
df_filtered.index.name = "date"

# Convert to time series for calmap
activity_series = df_filtered["games_played"]

# **Fix: Shift the start of the year to match the rolling 12-month window**
fig, ax = plt.subplots(figsize=(14, 4))
calmap.yearplot(activity_series, year=start_date.year, cmap="Greens", ax=ax, monthlabels="")

# Adjust x-axis labels to reflect the correct month order
months_order = pd.date_range(start=start_date, periods=12, freq="MS").strftime("%b")
ax.set_xticklabels(months_order, rotation=0)

ax.set_title(f"Chess Games Played Heatmap (Last 12 Months: {start_date} → {end_date})", fontsize=14)
plt.show()
