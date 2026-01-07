"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Soccer Team": {
        "description": "Join the school soccer team and compete in inter-school matches",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": [
            {"name": "Alex Johnson", "email": "alex@mergington.edu"},
            {"name": "James Smith", "email": "james@mergington.edu"}
        ]
    },
    "Basketball Club": {
        "description": "Practice basketball skills and participate in tournaments",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": [
            {"name": "Sarah Williams", "email": "sarah@mergington.edu"}
        ]
    },
    "Drama Club": {
        "description": "Participate in theater productions and develop acting skills",
        "schedule": "Wednesdays, 3:30 PM - 5:30 PM",
        "max_participants": 25,
        "participants": [
            {"name": "Emily Brown", "email": "emily@mergington.edu"},
            {"name": "Lucas Davis", "email": "lucas@mergington.edu"}
        ]
    },
    "Art Studio": {
        "description": "Explore various art mediums including painting, drawing, and sculpture",
        "schedule": "Fridays, 3:00 PM - 5:00 PM",
        "max_participants": 18,
        "participants": [
            {"name": "Mia Martinez", "email": "mia@mergington.edu"}
        ]
    },
    "Debate Team": {
        "description": "Develop critical thinking and public speaking through competitive debates",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": [
            {"name": "Noah Garcia", "email": "noah@mergington.edu"},
            {"name": "Ava Rodriguez", "email": "ava@mergington.edu"}
        ]
    },
    "Science Olympiad": {
        "description": "Compete in science competitions and conduct experiments",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": [
            {"name": "Liam Wilson", "email": "liam@mergington.edu"}
        ]
    },
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": [
            {"name": "Michael Anderson", "email": "michael@mergington.edu"},
            {"name": "Daniel Thomas", "email": "daniel@mergington.edu"}
        ]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": [
            {"name": "Emma Taylor", "email": "emma@mergington.edu"},
            {"name": "Sophia Moore", "email": "sophia@mergington.edu"}
        ]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": [
            {"name": "John Jackson", "email": "john@mergington.edu"},
            {"name": "Olivia White", "email": "olivia@mergington.edu"}
        ]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]
    # Validate student is not already signed up
    if any(p["email"] == email for p in activity["participants"]):
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")
    
    # Extract name from email (simple approach)
    name = email.split('@')[0].replace('.', ' ').title()
    
    # Add student
    activity["participants"].append({"name": name, "email": email})
    return {"message": f"Signed up {email} for {activity_name}"}
