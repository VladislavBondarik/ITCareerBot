CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    answers TEXT,
    specialty TEXT,
    feedback INTEGER DEFAULT 0
);