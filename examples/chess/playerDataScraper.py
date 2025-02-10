from chessdotcom import ChessDotComClient
import json
from pprint import pprint
from datetime import datetime, timezone
import pickle

   
client = ChessDotComClient(user_agent = "My Python Application...")

def getStartDate(username):
    startDate = client.get_player_profile(username).player.joined_datetime

    date_str = startDate.strftime("%Y-%m-%d %H:%M:%S")
    year, month, _ = date_str.split(" ")[0].split("-")
    return int(year), int(month)

def scapeData(username, startDate, endDate):
    all_data = []


    for year in range(startDate[0], endDate[0]+1):
        print("🗓️ SCRAPING DATA FROM : ", year)
        if(year == startDate[0]):
            month = startDate[1]
        else: month = 1
        while(month <=12):
            if(year == endDate[0] and month == int(endDate[1])+1): break
            userData = client.get_player_games_by_month(username, year=year, month=month)
            all_data.append(userData.json)
            month = month + 1
        break
    
    print(f"✅ Data scraping complete! Saved as")
    return all_data
    #file_path = f"/Users/shashankshriram/Downloads/preswald/examples/chess/{username}Data.pkl"
    #with open(file_path, "wb") as file:
    #    pickle.dump(all_data, file)



def refineData(all_data):
    """Refines chess data from a list of scraped data into a structured PKL format."""
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

    # Define the output file name dynamically
    output_file = f"/Users/shashankshriram/Downloads/preswald/examples/chess/{username}FormatedData.pkl"

    # Save the refined data as a pickle file
    with open(output_file, "wb") as file:
        pickle.dump(refined_data, file)

    print(f"✅ Refined data saved to {output_file}")
    return output_file



def main():
    ## TODO: ask for username and then run datascaping
    username = input("USERNAME : ")
    username = "fabianocaruana"## temp REMOVE LATER

    today = datetime.today()
    
    endDate = today.year, today.month
    startDate = getStartDate(username = username)
    

    refineData(all_data=scapeData(username = username, startDate= startDate, endDate=endDate))


if __name__ == '__main__':
    main()