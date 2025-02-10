import pickle
import json

def load_pickle(file_path):
    """Loads and prints the contents of a pickle file."""
    try:
        with open(file_path, "rb") as file:
            data = pickle.load(file)  # Load Pickle File
        print("✅ Pickle file loaded successfully!")
        return data
    except FileNotFoundError:
        print("❌ Error: Pickle file not found.")
    except Exception as e:
        print(f"❌ Error loading pickle file: {e}")

# Example usage
file_path = "/Users/shashankshriram/Downloads/preswald/examples/chess/FabianoCaruanaFormatedData.pkl"
data = load_pickle(file_path)




with open("output.json", "w") as json_file:
    json.dump(data, json_file, indent=4)
