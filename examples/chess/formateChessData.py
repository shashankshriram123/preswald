import pickle
import json
from datetime import datetime, timezone

# Load the PKL file
input_file = "/Users/shashankshriram/Downloads/preswald/examples/chess/fabianocaruanaData.pkl"  # Change this to your actual PKL file path
output_file = "/Users/shashankshriram/Downloads/preswald/examples/chess/refined_output.json"

def refine_chess_data(input_file, output_file):
    """Refines chess data from a pickle file into a structured JSON format."""
    # Load the pickle file
    with open(input_file, "rb") as file:
        chess_data = pickle.load(file)  # Load data from .pkl file

    # Extract primary username (assuming the user is always white in the first game)
    username = chess_data[0]["games"][0]["white"]["username"]
    
    refined_data = {
        "Username": username,
        "Data last updated": datetime.today().strftime('%Y-%m-%d'),
        "game_specific_data": []
    }

    for game in chess_data[0]["games"]:
        # Determine player color, opponent, and result
        if game["white"]["username"] == username:
            player_color = "white"
            opponent = game["black"]["username"]
            result = game["white"]["result"]
        else:
            player_color = "black"
            opponent = game["white"]["username"]
            result = game["black"]["result"]

        # Append game data with a timezone-aware datetime
        refined_data["game_specific_data"].append({
            "date": datetime.fromtimestamp(game["end_time"], tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
            "player color": player_color,
            "opponent": opponent,
            "result": result
        })

    # Save the refined JSON file
    with open(output_file, "w") as file:
        json.dump(refined_data, file, indent=4)

    print(f"✅ Refined data saved to {output_file}")

# Run the function
refine_chess_data(input_file, output_file)
