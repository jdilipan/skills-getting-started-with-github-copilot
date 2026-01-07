"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
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


class SignupRequest(BaseModel):
    name: str
    email: str


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
async def signup_for_activity(activity_name: str, req: SignupRequest):
    """Sign up a student for an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity = activities[activity_name]
    if any(p["email"] == req.email for p in activity["participants"]):
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")
    activity["participants"].append({"name": req.name, "email": req.email})
    return {"message": f"Signed up {req.email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str = Query(...)):
    """Remove a participant from an activity by email"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity = activities[activity_name]
    before_count = len(activity["participants"])
    activity["participants"] = [p for p in activity["participants"] if p["email"] != email]
    if len(activity["participants"]) == before_count:
        raise HTTPException(status_code=404, detail="Participant not found")
    return {"message": f"Unregistered {email} from {activity_name}"}
