import json
import os




def loadFile(filePath):
    #Loads the playlist from a JSON file. Returns an empty list if file missing.
    if not os.path.exists(filePath):
        return {}

    try:
        with open(filePath, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        print("Error loading playlist. Returning empty list.")
        return {}


def saveFile(filePath, data):
    # Saves the playlist to a JSON file.
    try:
        with open(filePath, "w") as file:
            json.dump(data, file, indent=4)
        print(f"saved {filePath} successfully.")
    except IOError:
        print("Error saving.")
