from preswald import plotly, table, text
import os
import duckdb

# Welcome message
text("# Welcome to Preswald!")
text("This is your Chess Data Dashboard. ♟️")

motherduck_token = os.getenv("MOTHERDUCK_TOKEN")

if motherduck_token:
    # Connect to the correct database
    database_name = "chess_duck_database"
    con = duckdb.connect(f"md:{database_name}?token={motherduck_token}")
    text(f"✅ Connected to {database_name} successfully!")

    # Fetch top players by followers
    players_data = con.execute("""
        SELECT username, name, title, followers 
        FROM players ORDER BY followers DESC LIMIT 10;
    """).fetchdf()
    
    # Display player table in Preswald
    text("### 🏆 Top 10 Most Followed Players")
    table(players_data)

    # Fetch rating stats for the top player
    top_player = players_data.iloc[0]["username"]
    rating_data = con.execute(f"""
        SELECT format, last_rating, best_rating 
        FROM ratings WHERE player_id = (
            SELECT player_id FROM players WHERE username = '{top_player}'
        );
    """).fetchdf()

    text(f"### 📊 {top_player}'s Rating History")
    table(rating_data)

else:
    text("❌ Error: MOTHERDUCK_TOKEN is not set.")
