import json
import os
import sqlite3, hashlib



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








conn = sqlite3.connect("user.db")  # creates file if not exists
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()


def login_check(username):
    cursor.execute(
    "SELECT * FROM users WHERE username = ?",
    (username,)
    )

    user = cursor.fetchone()
    print(user)
    return user


def register(username, password):
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        print("User registered successfully")
    except sqlite3.IntegrityError:
        print("Username already exists")


def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()