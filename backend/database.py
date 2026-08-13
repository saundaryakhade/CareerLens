import os
import sqlite3
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "skillgap.db")
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DB_DIR, exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS careers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        category TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS career_skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        career TEXT NOT NULL,
        skill TEXT NOT NULL,
        category TEXT,
        importance INTEGER DEFAULT 3,
        prerequisite TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skill_resources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        skill TEXT NOT NULL,
        resource_type TEXT,
        resource_name TEXT,
        description TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_skills TEXT,
        predicted_career TEXT,
        ml_confidence REAL,
        skill_match_score REAL,
        source_type TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()

    # Import initial data from CSV if tables are empty
    cursor.execute("SELECT COUNT(*) FROM career_skills")
    if cursor.fetchone()[0] == 0:
        cs_csv = os.path.join(DATA_DIR, "career_skills.csv")
        if os.path.exists(cs_csv):
            df_cs = pd.read_csv(cs_csv)
            for _, row in df_cs.iterrows():
                cursor.execute("""
                    INSERT INTO career_skills (career, skill, category, importance, prerequisite)
                    VALUES (?, ?, ?, ?, ?)
                """, (row['career'], row['skill'], row['category'], int(row['importance']), str(row['prerequisite']) if pd.notna(row['prerequisite']) else ""))
                
                cursor.execute("INSERT OR IGNORE INTO careers (name) VALUES (?)", (row['career'],))
                cursor.execute("INSERT OR IGNORE INTO skills (name, category) VALUES (?, ?)", (row['skill'], row['category']))

    cursor.execute("SELECT COUNT(*) FROM skill_resources")
    if cursor.fetchone()[0] == 0:
        sr_csv = os.path.join(DATA_DIR, "skill_resources.csv")
        if os.path.exists(sr_csv):
            df_sr = pd.read_csv(sr_csv)
            for _, row in df_sr.iterrows():
                cursor.execute("""
                    INSERT INTO skill_resources (skill, resource_type, resource_name, description)
                    VALUES (?, ?, ?, ?)
                """, (row['skill'], row['resource_type'], row['resource_name'], row['description']))

    conn.commit()
    conn.close()
    print("Database initialized successfully at", DB_PATH)

if __name__ == "__main__":
    init_db()
