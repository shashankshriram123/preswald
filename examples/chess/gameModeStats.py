from chessdotcom import ChessDotComClient
import json

client = ChessDotComClient(user_agent="My Python Application...")

# Fetch player statistics
userData = client.get_player_stats("avi-opening")
gameModeData = userData.json
print(json.dumps(gameModeData, indent=4))
#response = client.get_player_profile("fabianocaruana")
# Extract JSON response

#profileData = response.json

# Print the full JSON response (optional, for debugging)
# print(json.dumps(data, indent=4))

# Extract and print record of game stats

#print(json.dumps(profileData, indent=4))
