import json
from collections import defaultdict
from datetime import datetime

def aggregate_chess_data(data):
    """Aggregates chess data from a JSON file."""

    # Dictionary to store aggregated data
    aggregated_data = defaultdict(lambda: {
        "games_played": 0,
        "times_played_white": 0,
        "times_played_black": 0,
        "wins": 0,
        "checkmated": 0,
        "stalemates": 0,
        "resigned": 0
    })

    # Ensure we're working with a list of games
    if isinstance(data, dict) and "game_specific_data" in data:
        games = data["game_specific_data"]
    elif isinstance(data, list):
        games = data
    else:
        raise ValueError("Unexpected JSON structure!")

    # Process each game entry
    for game in games:
        if not isinstance(game, dict):
            continue  # Skip entries that are not dicts

        date_str = game.get("date")
        result = game.get("result")
        color = game.get("player color")

        # Convert date to YYYY-MM-DD format
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            date = date_obj.date().isoformat()
        except ValueError:
            print(f"Skipping invalid date: {date_str}")
            continue

        # Update stats
        aggregated_data[date]["games_played"] += 1
        if color == "white":
            aggregated_data[date]["times_played_white"] += 1
        elif color == "black":
            aggregated_data[date]["times_played_black"] += 1

        if result == "win":
            aggregated_data[date]["wins"] += 1
        elif result == "checkmated":
            aggregated_data[date]["checkmated"] += 1
        elif result == "stalemate":
            aggregated_data[date]["stalemates"] += 1
        else:
            aggregated_data[date]["resigned"] += 1

    # Convert to list for easier processing
    final_data = [{"date": date, **stats} for date, stats in aggregated_data.items()]

    return {"activity": final_data}
