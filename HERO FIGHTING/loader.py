import json
import os
import sqlite3
import hashlib


def loadFile(filePath):
    """Loads the playlist from a JSON file. Returns an empty dict if file missing."""
    if not os.path.exists(filePath):
        return {}

    try:
        with open(filePath, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        print("Error loading playlist. Returning empty list.")
        return {}


def saveFile(filePath, data):
    """Saves the playlist to a JSON file."""
    try:
        with open(filePath, "w") as file:
            json.dump(data, file, indent=4)
        print(f"saved {filePath} successfully.")
    except IOError:
        print("Error saving.")


# Initialize database directories
os.makedirs("database", exist_ok=True)

# Delete old database files to ensure clean schema
old_user_db = "database/user_data/user.db"
old_info_db = "database/user_info/user_info_store.db"

if os.path.exists(old_user_db):
    try:
        os.remove(old_user_db)
        print("[DB] Removed old user.db")
    except Exception as e:
        print(f"[DB] Could not remove old user.db: {e}")

if os.path.exists(old_info_db):
    try:
        os.remove(old_info_db)
        print("[DB] Removed old user_info_store.db")
    except Exception as e:
        print(f"[DB] Could not remove old user_info_store.db: {e}")

# Create SINGLE consolidated database with both tables
db_path = "database/game.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Create user_info table with all game stats
cursor.execute("""
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
    games_lost INTEGER DEFAULT 0,
    FOREIGN KEY(id) REFERENCES users(id)
)
""")

conn.commit()
print("[DB] Consolidated database initialized (database/game.db)")
print("[DB] Users table created/verified")
print("[DB] User_info table created/verified with all columns")


# Database functions

def login_check(username):
    """Check if user exists in database"""
    try:
        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()
        return user
    except Exception as e:
        print(f"[DB] Error checking login: {e}")
        return None


def register(username, password):
    """Register a new user"""
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        print(f"[DB] User '{username}' registered successfully")

        # Get the new user ID
        user_id = cursor.lastrowid
        
        # Create user info record with default stats
        cursor.execute(
            "INSERT INTO user_info (id, games_played, games_won, games_lost) VALUES (?, 0, 0, 0)",
            (user_id,)
        )
        conn.commit()
        print(f"[DB] User info created for user {user_id}")
        return True
        
    except sqlite3.IntegrityError as e:
        print(f"[DB] Username '{username}' already exists or registration failed: {e}")
        return False
    except Exception as e:
        print(f"[DB] Error during registration: {e}")
        return False


def show_all_user():
    """Display all registered users and their stats"""
    try:
        cursor.execute("SELECT id, username FROM users")
        users = cursor.fetchall()
        print("\n[DB] All Users:")
        for user in users:
            print(f"  ID: {user[0]}, Username: {user[1]}")
        
        cursor.execute("SELECT id, games_played, games_won, games_lost FROM user_info")
        stats = cursor.fetchall()
        print("\n[DB] User Stats:")
        for stat in stats:
            print(f"  ID: {stat[0]}, Games: {stat[1]}, Won: {stat[2]}, Lost: {stat[3]}")
    except Exception as e:
        print(f"[DB] Error showing users: {e}")


def get_leaderboard_data():
    """Get all users with their game stats for the leaderboard, sorted by wins"""
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
        print(f"[DB] Leaderboard query returned {len(results)} users")
        return results
    except Exception as e:
        print(f"[DB] Error fetching leaderboard: {e}")
        return []


def update_user_win(user_id):
    """Increment wins and games_played for a user"""
    try:
        cursor.execute("""
            UPDATE user_info 
            SET games_won = COALESCE(games_won, 0) + 1,
                games_played = COALESCE(games_played, 0) + 1
            WHERE id = ?
        """, (user_id,))
        conn.commit()
        print(f"[DB] User {user_id} win recorded")
        return True
    except Exception as e:
        print(f"[DB] Error updating user win: {e}")
        return False


def update_user_loss(user_id):
    """Increment losses and games_played for a user"""
    try:
        cursor.execute("""
            UPDATE user_info 
            SET games_lost = COALESCE(games_lost, 0) + 1,
                games_played = COALESCE(games_played, 0) + 1
            WHERE id = ?
        """, (user_id,))
        conn.commit()
        print(f"[DB] User {user_id} loss recorded")
        return True
    except Exception as e:
        print(f"[DB] Error updating user loss: {e}")
        return False


def get_user_stats(user_id):
    """Get a specific user's game stats"""
    try:
        cursor.execute("""
            SELECT games_played, games_won, games_lost
            FROM user_info
            WHERE id = ?
        """, (user_id,))
        result = cursor.fetchone()
        if result:
            return {
                'games_played': result[0] or 0,
                'games_won': result[1] or 0,
                'games_lost': result[2] or 0
            }
        return None
    except Exception as e:
        print(f"[DB] Error fetching user stats: {e}")
        return None


def hash_pw(pw):
    """Hash a password using SHA256"""
    return hashlib.sha256(pw.encode()).hexdigest()


# Print completion message
print("[DB] Database system initialized successfully!")
