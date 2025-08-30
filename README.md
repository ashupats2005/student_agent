# Student Agent – Flask Student Profile Manager

A web application for managing student profiles, skills, projects, and education, built with Flask and SQLite and deployed via Docker on Railway.

## Features

- **Student Dashboard:** Visualize and manage student records  
- **CRUD API:** Create, Read, Update, Delete student profiles  
- **Skills & Projects Browsing:** List top skills, filter projects by skill  
- **Seed Data:** Default student data loaded on first launch  
- **Easy Deployment:** Containerized with Docker and deploys on Railway

## Tech Stack

- **Backend:** Python (Flask, flask-cors, requests)  
- **Database:** SQLite  
- **Frontend:** HTML templates (Jinja2)  
- **DevOps:** Docker, Railway

## Setup & Installation

### Prerequisites

- Python 3.8 or higher  
- Docker installed (for local container builds)  
- A Railway account

### Local Development

git clone https://github.com/ashupats2005/student_agent.git
cd student_agent
docker-compose build student_agent
docker-compose up
pip install -r requirements.txt


### Deploy to Railway

1. Push your code to GitHub.
2. On Railway, create a new project and choose “Deploy from Dockerfile” or use your DockerHub image (e.g. `ashuaitech/student_agent:latest`).
3. Set environment variables as needed. Make sure `PORT` is mapped or the Docker CMD uses it.
4. Railway will build and deploy your app. Your public URL will be generated.

## API Endpoints

| Route                      | Method | Description                   |
|----------------------------|--------|-------------------------------|
| `/`                        | GET    | Main dashboard/homepage       |
| `/central_app`             | GET    | Student dashboard             |
| `/student/create`          | POST   | Create a new student profile  |
| `/student/<student_id>`    | GET    | Get details of a student      |
| `/student/<student_id>`    | PUT    | Update a profile              |
| `/student/<student_id>`    | DELETE | Delete a profile              |
| `/student/all`             | GET    | List all profiles             |
| `/projects`                | GET    | Filter projects by skill      |
| `/skills/top`              | GET    | Show top skills               |
| `/search`                  | GET    | Search profiles               |
| `/health`                  | GET    | Health check/test             |

## Seed Data

Initial student profiles, skills, and project data are loaded from `seed.sql` and displayed via the UI for demo/testing purposes.

## Folder Structure

student_agents/
├── student_agent.py
├── registration.py
├── requirements.txt
├── Dockerfile
├── schema.sql
├── seed.sql
├── data/
│ └── student.db
├── templates/
│ └── student_dashboard.html





