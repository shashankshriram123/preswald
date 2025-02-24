from preswald import plotly, table, text
import os
import duckdb
import pandas as pd
import plotly.graph_objects as go

def generate_heatmap():
    motherduck_token = os.getenv("MOTHERDUCK_TOKEN")
    if not motherduck_token:
        raise ValueError("❌ MOTHERDUCK_TOKEN not set.")

    con = duckdb.connect(f"md:chess_duck_database?token={motherduck_token}")

    years = [
        int(r[0]) for r in con.execute("""
            SELECT DISTINCT strftime('%Y', date) AS year
            FROM activity_logs
            ORDER BY year DESC;
        """).fetchall()
    ]

    df = con.execute("""
        SELECT player_id, date, games_played
        FROM activity_logs
        WHERE player_id = (
            SELECT player_id FROM players ORDER BY followers DESC LIMIT 1
        );
    """).fetchdf()

    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["week"] = df["date"].dt.strftime("%U").astype(int)
    df["weekday"] = df["date"].dt.weekday

    def create_full_year_df(year):
        rng = pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31", freq="D")
        out = pd.DataFrame({
            "date": rng,  # Added date column
            "year": rng.year,
            "week": rng.strftime("%U").astype(int),
            "weekday": rng.weekday,
            "games_played": 0
        })
        return out

    fig = go.Figure()
    x_tickvals, x_ticktext = None, None

    for i, year in enumerate(years):
        full_year = create_full_year_df(year)
        full_year['month'] = full_year['date'].dt.month
        week_month = full_year.groupby('week')['month'].first().reset_index()
        
        months_in_order = []
        current_month = None
        for _, row in week_month.iterrows():
            if row['month'] != current_month:
                current_month = row['month']
                months_in_order.append({'week': row['week'], 'month': current_month})
        
        tickvals = [m['week'] for m in months_in_order]
        ticktext = [pd.Timestamp(year=year, month=m['month'], day=1).strftime('%b') for m in months_in_order]
        
        if i == 0:
            x_tickvals = tickvals
            x_ticktext = ticktext

        merged = pd.concat([full_year, df[df["year"] == year]], ignore_index=True)
        grouped = merged.groupby(["weekday", "week"], as_index=False)["games_played"].sum()
        pivoted = grouped.pivot(index="weekday", columns="week", values="games_played").fillna(0)

        fig.add_trace(go.Heatmap(
            z=pivoted.values,
            x=pivoted.columns,
            y=pivoted.index,
            colorscale="Greens",
            xgap=2,
            ygap=2,
            showscale=False,
            visible=(i == 0)
        ))

    cell_size = 30
    fig_width = cell_size * 53  # Adjusted for 53 weeks
    fig_height = cell_size * 7

    fig.update_layout(
        title=f"{years[0]} Chess Activity Heatmap",
        width=fig_width,
        height=fig_height,
        autosize=False,
        margin=dict(l=30, r=30, t=40, b=40),
        updatemenus=[dict(
            buttons=[dict(
                label=str(y),
                method="update",
                args=[
                    {"visible": [j == i for j in range(len(years))]},
                    {"title": f"{y} Chess Activity Heatmap"}
                ]
            ) for i, y in enumerate(years)],
            direction="down",
            x=1.0,
            y=1.1,
            xanchor="right",
            yanchor="bottom",
            showactive=True
        )],
        xaxis=dict(
            range=[0, 52],
            visible=True,
            tickvals=x_tickvals,
            ticktext=x_ticktext
        ),
        yaxis=dict(
            tickvals=[0, 1, 2, 3, 4, 5, 6],
            ticktext=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            visible=True
        ),
        plot_bgcolor="#fff"
    )

    return fig

text("# Chess Heatmap with Axis Labels")

if os.getenv("MOTHERDUCK_TOKEN"):
    con = duckdb.connect(f"md:chess_duck_database?token={os.getenv('MOTHERDUCK_TOKEN')}")
    text("✅ Connected to chess_duck_database successfully!")
    fig = generate_heatmap()
    plotly(fig)
else:
    text("❌ Error: MOTHERDUCK_TOKEN is not set.")