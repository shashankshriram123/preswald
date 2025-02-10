from chessdotcom import ChessDotComClient
import json
from pprint import pprint
from datetime import datetime
import pickle

   
client = ChessDotComClient(user_agent = "My Python Application...")

def getStartDate(username):
    startDate = client.get_player_profile(username).player.joined_datetime

    date_str = startDate.strftime("%Y-%m-%d %H:%M:%S")
    year, month, _ = date_str.split(" ")[0].split("-")
    return int(year), int(month)

def scapeDate(username, startDate, endDate):
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
    
    file_path = f"/Users/shashankshriram/Downloads/preswald/examples/chess/{username}Data.pkl"
    with open(file_path, "wb") as file:
        pickle.dump(all_data, file)

    print(f"✅ Data scraping complete! Saved as {file_path}")

def main():
    ## TODO: ask for username and then run datascaping
    username = input("USERNAME : ")
    username = "fabianocaruana"## temp REMOVE LATER

    today = datetime.today()
    
    endDate = today.year, today.month
    startDate = getStartDate(username = username)
    scapeDate(username = username, startDate= startDate, endDate=endDate)




if __name__ == '__main__':
    main()