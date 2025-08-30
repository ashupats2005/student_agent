# Database Schema

This document describes the schema for the `student_profile` table used in the Student Agent application.

## student_profile Table

| Column    | Data Type | Description                              |
|-----------|------------|------------------------------------------|
| id        | TEXT (UUID) | Unique identifier for each student profile |
| name      | TEXT       | Full name of the student                  |
| email     | TEXT       | Email address of the student              |
| education | TEXT       | JSON-encoded list of education records   |
| skills    | TEXT       | JSON-encoded list of skills               |
| projects  | TEXT       | JSON-encoded list of projects             |
| work      | TEXT       | JSON-encoded list of work experiences     |
| links     | TEXT       | JSON-encoded dictionary of external links (e.g., LinkedIn, GitHub) |

---

## Notes

- The fields `education`, `skills`, `projects`, `work`, and `links` are stored as JSON-encoded strings in the database but are parsed as lists or dictionaries in the application logic.
- The `id` is generated as a UUID string to ensure uniqueness.
- The database is implemented using SQLite and is initialized through the `schema.sql` and `seed.sql` scripts.

---

## Example schema.sql snippet

```sql
CREATE TABLE student_profile (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    education TEXT,
    skills TEXT,
    projects TEXT,
    work TEXT,
    links TEXT
);
