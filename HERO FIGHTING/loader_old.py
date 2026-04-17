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







os.makedirs("database/user_data", exist_ok=True)
os.makedirs("database/user_info", exist_ok=True)

# Delete old database files to recreate with proper schema
old_db_path = "database/user_data/user.db"
old_db_info_path = "database/user_info/user_info_store.db"

if os.path.exists(old_db_path):
    try:
        os.remove(old_db_path)
        print("Removed old user.db to recreate with proper schema")
    except Exception as e:
        print(f"Could not remove old database: {e}")

if os.path.exists(old_db_info_path):
    try:
        os.remove(old_db_info_path)
        print("Removed old user_info_store.db to recreate with proper schema")
    except Exception as e:
        print(f"Could not remove old database: {e}")

conn = sqlite3.connect("database/user_data/user.db")  # creates file if not exists
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()


conn2 = sqlite3.connect("database/user_info/user_info_store.db")

cursor2 = conn2.cursor()

cursor2.execute("""
CREATE TABLE IF NOT EXISTS user_info (
    id INTEGER PRIMARY KEY,
    volume REAL DEFAULT 1.0,
    text_anti_aliasing INTEGER DEFAULT 0,
    smooth_background INTEGER DEFAULT 0,
    show_distance INTEGER DEFAULT 0,
    show_hitbox INTEGER DEFAULT 0,
    show_ground INTEGER DEFAULT 0,
    games_played INTEGER DEFAULT 0,
    games_won INTEGER DEFAULT 0,
    games_lost INTEGER DEFAULT 0
)
""")
conn2.commit()

print("Database initialized successfully with all required columns")


try:
    cursor2.execute("ALTER TABLE user_info ADD COLUMN games_won INTEGER DEFAULT 0")
except sqlite3.OperationalError:
    pass  # Column already exists

try:
    cursor2.execute("ALTER TABLE user_info ADD COLUMN games_lost INTEGER DEFAULT 0")
except sqlite3.OperationalError:
    pass  # Column already exists

conn2.commit()





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

        user_id = cursor.lastrowid
        cursor2.execute(
            "INSERT INTO user_info (id) VALUES (?)",
            (user_id,)
        )
        conn2.commit()
        return True
        
    except sqlite3.IntegrityError:
        print("Username already exists")
        return False

def show_all_user():
    cursor.execute("SELECT * FROM users")
    print(cursor.fetchall())
    
    cursor2.execute("SELECT * FROM user_info")
    print(cursor2.fetchall())


def get_leaderboard_data():
    """Get all users with their game stats for the leaderboard"""
    try:
        cursor.execute("""
            SELECT u.id, u.username, 
                   COALESCE(i.games_played, 0) as games_played,
                   COALESCE(i.games_won, 0) as games_won,
                   COALESCE(i.games_lost, 0) as games_lost
            FROM users u
            LEFT JOIN user_info i ON u.id = i.id
            ORDER BY COALESCE(i.games_won, 0) DESC, COALESCE(i.games_played, 0) DESC
        """)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"Error fetching leaderboard: {e}")
        return []


def update_user_win(user_id):
    """Increment wins and games_played for a user"""
    try:
        cursor2.execute("""
            UPDATE user_info 
            SET games_won = COALESCE(games_won, 0) + 1,
                games_played = COALESCE(games_played, 0) + 1
            WHERE id = ?
        """, (user_id,))
        conn2.commit()
        print(f"User {user_id} win recorded")
        return True
    except Exception as e:
        print(f"Error updating user win: {e}")
        return False


def update_user_loss(user_id):
    """Increment losses and games_played for a user"""
    try:
        cursor2.execute("""
            UPDATE user_info 
            SET games_lost = COALESCE(games_lost, 0) + 1,
                games_played = COALESCE(games_played, 0) + 1
            WHERE id = ?
        """, (user_id,))
        conn2.commit()
        print(f"User {user_id} loss recorded")
        return True
    except Exception as e:
        print(f"Error updating user loss: {e}")
        return False


def get_user_stats(user_id):
    """Get a specific user's game stats"""
    try:
        cursor2.execute("""
            SELECT games_played, games_won, games_lost
            FROM user_info
            WHERE id = ?
        """, (user_id,))
        result = cursor2.fetchone()
        if result:
            return {
                'games_played': result[0] or 0,
                'games_won': result[1] or 0,
                'games_lost': result[2] or 0
            }
        return None
    except Exception as e:
        print(f"Error fetching user stats: {e}")
        return None

    
def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()


print(cursor.fetchall)