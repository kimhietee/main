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
        return {}


def saveFile(filePath, data):
    """Saves the playlist to a JSON file."""
    try:
        with open(filePath, "w") as file:
            json.dump(data, file, indent=4)
    except IOError:
        pass


# Initialize database directories
os.makedirs("database", exist_ok=True)

# Delete old database files to ensure clean schema
old_user_db = "database/user_data/user.db"
old_info_db = "database/user_info/user_info_store.db"

if os.path.exists(old_user_db):
    try:
        os.remove(old_user_db)
    except Exception as e:
        pass

if os.path.exists(old_info_db):
    try:
        os.remove(old_info_db)
    except Exception as e:
        pass

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
        return None


def register(username, password):
    """Register a new user"""
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()

        # Get the new user ID
        user_id = cursor.lastrowid
        
        # Create user info record with default stats
        cursor.execute(
            "INSERT INTO user_info (id, games_played, games_won, games_lost) VALUES (?, 0, 0, 0)",
            (user_id,)
        )
        conn.commit()
        return True
        
    except sqlite3.IntegrityError as e:
        return False
    except Exception as e:
        return False


def show_all_user():
    """Display all registered users and their stats"""
    try:
        cursor.execute("SELECT id, username FROM users")
        users = cursor.fetchall()
        for user in users:
            pass
        
        cursor.execute("SELECT id, games_played, games_won, games_lost FROM user_info")
        stats = cursor.fetchall()
        for stat in stats:
            pass
    except Exception as e:
        pass


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
        return results
    except Exception as e:
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
        return True
    except Exception as e:
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
        return True
    except Exception as e:
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
        return None


def hash_pw(pw):
    """Hash a password using SHA256"""
    return hashlib.sha256(pw.encode()).hexdigest()
