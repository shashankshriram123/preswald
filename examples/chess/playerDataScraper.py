from chessdotcom import ChessDotComClient
import json
from pprint import pprint
from datetime import datetime, timezone
import pickle
from aggregateUserData import aggregate_chess_data  # ✅ Import the function

client = ChessDotComClient(user_agent="My Python Application...")

def getStartDate(username):
    startDate = client.get_player_profile(username).player.joined_datetime
    date_str = startDate.strftime("%Y-%m-%d %H:%M:%S")
    year, month, _ = date_str.split(" ")[0].split("-")
    return int(year), int(month)

def scapePlayerGameModeStats(username):
    print(f"🔄 Fetching game statistics for user: {username}...")
    try:
        userData = client.get_player_stats(username)
        gameModeData = userData.json
        print("✅ Game statistics successfully retrieved.")
        return gameModeData
    except Exception as e:
        print(f"❌ Failed to retrieve stats: {e}")
        return None

def scrapePlayerProfile(username):
    print(f"🔄 Fetching player profile for user: {username}...")
    try:
        userData = client.get_player_profile(username)
        profileData = userData.json
        print("✅ Player profile successfully retrieved.")
        return profileData
    except Exception as e:
        print(f"❌ Failed to retrieve player profile: {e}")
        return None

def scapePlayerActivityData(username, startDate, endDate):
    all_data = []

    for year in range(startDate[0], endDate[0] + 1):
        print("🗓️ SCRAPING ACTIVITY DATA FROM:", year)
        if year == startDate[0]:
            month = startDate[1]
        else:
            month = 1
        while month <= 12:
            if year == endDate[0] and month == int(endDate[1]) + 1:
                break
            
            try:
                userData = client.get_player_games_by_month(username, year=year, month=month)
                response_json = userData.json
                
                # Ensure there is valid game data before adding
                if "games" in response_json and response_json["games"]:
                    all_data.append(response_json)
                else:
                    print(f"⚠️ No data found for {year}-{month:02d}, skipping.")
            
            except Exception as e:
                print(f"❌ Failed to retrieve data for {year}-{month:02d}: {e}")
            
            month += 1

    print("✅ Data scraping complete!")
    return all_data


def refineData(all_data):
    """Refines chess data from a list of scraped data into a structured format and returns a filtered array."""
    if not all_data or not all_data[0]["games"]:
        print("⚠️ No game data found!")
        return None

    # Extract primary username (assuming the user is always white in the first game)
    username = all_data[0]["games"][0]["white"]["username"]

    refined_data = {
        "Username": username,
        "Data last updated": datetime.today().strftime('%Y-%m-%d'),
        "game_specific_data": []
    }

    for entry in all_data:
        for game in entry["games"]:
            if game["white"]["username"] == username:
                player_color = "white"
                opponent = game["black"]["username"]
                result = game["white"]["result"]
            else:
                player_color = "black"
                opponent = game["white"]["username"]
                result = game["black"]["result"]

            refined_data["game_specific_data"].append({
                "date": datetime.fromtimestamp(game["end_time"], tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
                "player color": player_color,
                "opponent": opponent,
                "result": result
            })

    print("✅ Data refinement complete")
    return refined_data

def fixJSONformat(data):

    # Fix duplicate keys
    data["player"] = data["player"]["player"]
    data["stats"] = data["stats"]["stats"]
    data["activity"] = data["activity"]["activity"]

    # Convert timestamps to readable format
    def convert_timestamp(ts):
        return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    data["player"]["last_online"] = convert_timestamp(data["player"]["last_online"])
    data["player"]["joined"] = convert_timestamp(data["player"]["joined"])

    # Extract country code from URL
    data["player"]["country"] = data["player"]["country"].split("/")[-1]

    # Convert timestamps in chess stats
    for category in ["chess_rapid", "chess_bullet", "chess_blitz"]:
        if category in data["stats"]:
            data["stats"][category]["last"]["date"] = convert_timestamp(data["stats"][category]["last"]["date"])
            data["stats"][category]["best"]["date"] = convert_timestamp(data["stats"][category]["best"]["date"])

    data["stats"]["tactics"]["highest"]["date"] = convert_timestamp(data["stats"]["tactics"]["highest"]["date"])
    data["stats"]["tactics"]["lowest"]["date"] = convert_timestamp(data["stats"]["tactics"]["lowest"]["date"])

    return data


def main():
    username = input("USERNAME: ")
    username = "fabianocaruana"  # Temp, remove later

    today = datetime.today()
    endDate = today.year, today.month
    startDate = getStartDate(username=username)

    # Get player profile
    player_profile = scrapePlayerProfile(username=username)
    # Get game mode stats
    game_mode_stats = scapePlayerGameModeStats(username=username)

    
    # Get raw game data
    raw_data = scapePlayerActivityData(username=username, startDate=startDate, endDate=endDate)

    # Refine raw data
    refined_data = refineData(all_data=raw_data)


    # Aggregate data
    aggregated_data = aggregate_chess_data(refined_data)  # Call the function from aggregateUserData.py

    # Structure final JSON format
    final_data = {
        "player": player_profile,   # Player profile
        "stats": game_mode_stats,   # Game mode statistics
        "activity": aggregated_data  # Aggregated activity data
    }
    clean_data = fixJSONformat(final_data)

    # Save aggregated data as JSON
    aggregated_json_path = f"/Users/shashankshriram/Downloads/preswald/examples/chess/test_data/{username}AggregatedData.json"
    with open(aggregated_json_path, "w") as file:
        json.dump(clean_data, file, indent=4)

    print(f"✅ Aggregated data saved to {aggregated_json_path}")

if __name__ == '__main__':
    main()
