-- schema.sql
CREATE TABLE IF NOT EXISTS student_profile (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    education TEXT,
    skills TEXT,
    projects TEXT,
    work TEXT,
    links TEXT
);
