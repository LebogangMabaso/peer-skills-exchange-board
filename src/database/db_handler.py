import sqlite3
import json
from typing import List, Optional
from datetime import datetime
from src.models.user import User
from src.models.match import Match

class DatabaseHandler:
    def __init__(self, db_path: str = "peer_exchange.db"):
        self.db_path = db_path

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def initialize_database(self) -> None:
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    location TEXT,
                    bio TEXT,
                    created_at TEXT NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS skills_offered (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    skill TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    UNIQUE(user_id, skill)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS skills_needed (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    skill TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    UNIQUE(user_id, skill)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS matches (
                    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user1_id INTEGER NOT NULL,
                    user2_id INTEGER NOT NULL,
                    compatibility_score REAL NOT NULL,
                    matching_skills TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (user1_id) REFERENCES users (user_id),
                    FOREIGN KEY (user2_id) REFERENCES users (user_id),
                    UNIQUE(user1_id, user2_id)
                )
            """)

            conn.commit()

    def add_user(self, user: User) -> int:
        """Insert a new user into the database and return its ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO users (name, email, location, bio, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                user.name,
                user.email,
                user.location,
                user.bio,
                user.created_at.isoformat()
            ))

            user_id = cursor.lastrowid

            for skill in user.skills_offered:
                cursor.execute("""
                    INSERT OR IGNORE INTO skills_offered (user_id, skill)
                    VALUES (?, ?)
                """, (user_id, skill))

            for skill in user.skills_needed:
                cursor.execute("""
                    INSERT OR IGNORE INTO skills_needed (user_id, skill)
                    VALUES (?, ?)
                """, (user_id, skill))

            conn.commit()
            return user_id

    def get_user(self, user_id: int) -> Optional[User]:
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            user_row = cursor.fetchone()
            if not user_row:
                return None

            cursor.execute("SELECT skill FROM skills_offered WHERE user_id = ?", (user_id,))
            skills_offered = [row["skill"] for row in cursor.fetchall()]

            cursor.execute("SELECT skill FROM skills_needed WHERE user_id = ?", (user_id,))
            skills_needed = [row["skill"] for row in cursor.fetchall()]

            return User(
                user_id=user_row["user_id"],
                name=user_row["name"],
                email=user_row["email"],
                location=user_row["location"],
                bio=user_row["bio"],
                created_at=datetime.fromisoformat(user_row["created_at"]),
                skills_offered=skills_offered,
                skills_needed=skills_needed
            )

    def get_user_by_email(self, email: str) -> Optional[User]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM users WHERE email = ?", (email,))
            result = cursor.fetchone()
            if result:
                return self.get_user(result["user_id"])
            return None

    def get_all_users(self) -> List[User]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM users ORDER BY created_at")
            rows = cursor.fetchall()
            
            user_ids = []
            for row in rows:
                user_ids.append(row["user_id"])
            
            all_users = []
            for user_id in user_ids:
                user = self.get_user(user_id)
                if user:
                    all_users.append(user)
            
            return all_users

    def update_user(self, user: User) -> bool:
        if not user.user_id:
            return False

        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE users
                SET name = ?, email = ?, location = ?, bio = ?
                WHERE user_id = ?
            """, (user.name, user.email, user.location, user.bio, user.user_id))

            cursor.execute("DELETE FROM skills_offered WHERE user_id = ?", (user.user_id,))
            cursor.execute("DELETE FROM skills_needed WHERE user_id = ?", (user.user_id,))

            for skill in user.skills_offered:
                cursor.execute("INSERT INTO skills_offered (user_id, skill) VALUES (?, ?)",
                               (user.user_id, skill))

            for skill in user.skills_needed:
                cursor.execute("INSERT INTO skills_needed (user_id, skill) VALUES (?, ?)",
                               (user.user_id, skill))

            conn.commit()
            return cursor.rowcount > 0

    def delete_user(self, user_id: int) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("DELETE FROM skills_offered WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM skills_needed WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM matches WHERE user1_id = ? OR user2_id = ?", (user_id, user_id))
            cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))

            conn.commit()
            return cursor.rowcount > 0


    def save_match(self, match: Match) -> int:

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO matches
                (user1_id, user2_id, compatibility_score, matching_skills, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                match.user1_id,
                match.user2_id,
                match.compatibility_score,
                json.dumps(match.matching_skills),
                match.created_at.isoformat()
            ))
            conn.commit()
            return cursor.lastrowid

    def get_matches_for_user(self, user_id: int) -> List[Match]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM matches
                WHERE user1_id = ? OR user2_id = ?
                ORDER BY compatibility_score DESC
            """, (user_id, user_id))

            rows = cursor.fetchall()
            matches = []
            
            for row in rows:
                match = Match(
                    match_id=row["match_id"],
                    user1_id=row["user1_id"],
                    user2_id=row["user2_id"],
                    compatibility_score=row["compatibility_score"],
                    matching_skills=json.loads(row["matching_skills"]),
                    created_at=datetime.fromisoformat(row["created_at"])
                )
                matches.append(match)
            
            return matches
