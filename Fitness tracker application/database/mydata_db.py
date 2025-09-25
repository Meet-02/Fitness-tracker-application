import sqlite3

import os

# Get project root (parent of this file’s folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database folder (only one level)
db_dir = os.path.join(BASE_DIR, 'database')
os.makedirs(db_dir, exist_ok=True)

db_path = os.path.join(db_dir, 'mydata.db')

def create_tables():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Create workouts table
    cur.execute('''CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        duration INTEGER,
        calories INTEGER
    )''')

    # Create diets table
    cur.execute('''CREATE TABLE IF NOT EXISTS diets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        meal TEXT,
        calories INTEGER,
        protein INTEGER
    )''')

    # Create wearables table
    cur.execute('''CREATE TABLE IF NOT EXISTS wearables (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        heart_rate INTEGER,
        steps INTEGER,
        recorded_at TEXT
    )''')

    conn.commit()
    conn.close()
    print("✅ Tables created successfully in")

def init_db():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            duration INTEGER NOT NULL,
            calories INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    init_db()
