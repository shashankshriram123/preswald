import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Load data
data_file = "/Users/shashankshriram/Downloads/preswald/examples/chess/fabianocaruanaAggregatedData.json"
df = pd.read_json(data_file)

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Define the time range (past 365 days)
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# Filter data for the last year
df_filtered = df[(df["date"] >= start_date) & (df["date"] <= end_date)].copy()

# Ensure full coverage of 365 days (fill missing days with zeroes)
all_dates = pd.date_range(start=start_date, end=end_date, freq='D')
df_filtered = df_filtered.set_index("date").reindex(all_dates, fill_value=0).reset_index()
df_filtered.rename(columns={"index": "date"}, inplace=True)

# Extract week number and day of the week
df_filtered["week"] = df_filtered["date"].dt.isocalendar().week
df_filtered["weekday"] = df_filtered["date"].dt.weekday  # Monday = 0, Sunday = 6

# Create a blank 7x53 heatmap (7 days, 53 weeks)
heatmap_data = np.zeros((7, 53))

# Populate the heatmap array
for _, row in df_filtered.iterrows():
    week_idx = row["week"] - 1
    day_idx = row["weekday"]
    heatmap_data[day_idx, week_idx] = row["games_played"]  # Ensure this exists in your data

# Create the heatmap plot
fig, ax = plt.subplots(figsize=(15, 5))
c = ax.imshow(heatmap_data, cmap="Greens", aspect="auto")

# Set labels and titles
ax.set_title("Chess Player Activity Heatmap (Past 365 Days)")
ax.set_xlabel("Week of Year")
ax.set_ylabel("Day of Week")
ax.set_yticks(range(7))
ax.set_yticklabels(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])

# Format x-axis ticks
xticks = range(0, 53, 2)
ax.set_xticks(xticks)
ax.set_xticklabels(xticks, rotation=45)

# Add colorbar
fig.colorbar(c, ax=ax)

# Show the plot
plt.show()
