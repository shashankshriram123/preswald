import json
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, "chess_project/external/calmap")

import calmap

from datetime import datetime
from matplotlib.widgets import Button

# Load JSON data
json_file = "/Users/shashankshriram/Downloads/preswald/examples/chess/avi-openingAggregatedData.json"
with open(json_file, "r") as file:
    chess_data = json.load(file)

# Convert JSON into DataFrame
df = pd.DataFrame(chess_data)

# Ensure 'date' column is in datetime format
df["date"] = pd.to_datetime(df["date"])

# Get available years
available_years = sorted(df["date"].dt.year.unique(), reverse=True)
current_year = available_years[0]  # Start with the latest year

# Create figure
fig, ax = plt.subplots(figsize=(14, 4))
plt.subplots_adjust(bottom=0.2)  # Adjust space for buttons

# Function to plot heatmap for a selected year
def plot_yearly_heatmap(year):
    global current_year
    current_year = year
    ax.clear()
    
    df_filtered = df[df["date"].dt.year == year].copy()
    
    if df_filtered.empty:
        ax.set_title(f"❌ No data available for {year}", fontsize=14)
        plt.draw()
        return
    
    # Ensure all days in the year are represented
    all_dates = pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31", freq="D")
    df_filtered = df_filtered.set_index("date").reindex(all_dates, fill_value=0)
    df_filtered.index.name = "date"
    
    # Convert to time series for calmap
    activity_series = df_filtered["games_played"]
    
    # Plot heatmap
    calmap.yearplot(
        activity_series,
        year=year,
        cmap="Greens",
        ax=ax,
        daylabels=["", "Mon", "", "Wed", "", "Fri", ""],  # Show only Mon, Wed, Fri
        dayticks=[1, 3, 5]  # Index positions of Monday, Wednesday, Friday
    )
    ax.set_title(f"Chess Games Played Heatmap - {year}", fontsize=14)
    
    plt.draw()

# Button Callbacks
def prev(event):
    idx = available_years.index(current_year)
    if idx < len(available_years) - 1:
        plot_yearly_heatmap(available_years[idx + 1])

def next(event):
    idx = available_years.index(current_year)
    if idx > 0:
        plot_yearly_heatmap(available_years[idx - 1])

# Add buttons
axprev = plt.axes([0.3, 0.05, 0.1, 0.075])  # Previous button position
axnext = plt.axes([0.6, 0.05, 0.1, 0.075])  # Next button position

bprev = Button(axprev, '← Previous')
bnext = Button(axnext, 'Next →')

bprev.on_clicked(prev)
bnext.on_clicked(next)

# Show the latest year's heatmap initially
plot_yearly_heatmap(current_year)

plt.show(block=True)  # Ensure interactive mode stays open
