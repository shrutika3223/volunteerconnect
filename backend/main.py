from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import google.generativeai as genai
import os
from datetime import datetime
import json

app = FastAPI(title="VolunteerConnect API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# ─── Mock DB ────────────────────────────────────────────────────────────────

volunteers_db = [
    {"id": 1, "name": "Ananya Sharma", "skills": ["teaching", "mentoring"], "location": "Pune", "availability": "weekends", "hours_per_week": 5, "past_events": 12, "rating": 4.8},
    {"id": 2, "name": "Rohan Mehta",   "skills": ["medical", "first aid"],  "location": "Mumbai","availability": "evenings", "hours_per_week": 8, "past_events": 7,  "rating": 4.5},
    {"id": 3, "name": "Priya Iyer",    "skills": ["coding", "teaching"],    "location": "Bangalore","availability": "weekdays","hours_per_week": 10,"past_events": 20, "rating": 4.9},
    {"id": 4, "name": "Karan Patel",   "skills": ["logistics", "driving"],  "location": "Pune", "availability": "weekends", "hours_per_week": 6, "past_events": 5,  "rating": 4.2},
    {"id": 5, "name": "Sneha Kulkarni","skills": ["counseling", "teaching"],"location": "Pune", "availability": "weekends", "hours_per_week": 4, "past_events": 9,  "rating": 4.7},
]

events_db = [
    {"id": 1, "title": "Digital Literacy Camp",   "required_skills": ["teaching","coding"],  "location": "Pune",      "date": "2026-05-10", "slots": 3, "registered": 1},
    {"id": 2, "title": "Blood Donation Drive",     "required_skills": ["medical","first aid"],"location": "Mumbai",   "date": "2026-05-15", "slots": 5, "registered": 2},
    {"id": 3, "title": "Rural School Support",     "required_skills": ["teaching","mentoring"],"location": "Pune",    "date": "2026-05-20", "slots": 4, "registered": 0},
    {"id": 4, "title": "Food Distribution Drive",  "required_skills": ["logistics","driving"], "location": "Bangalore","date": "2026-05-25", "slots": 6, "registered": 3},
]

impact_data = {
    "total_volunteers": 1240,
    "total_events": 87,
    "total_hours": 9800,
    "beneficiaries": 42000,
    "cities_covered": 12,
}

# ─── Models ──────────────────────────────────────────────────────────────────

class MatchRequest(BaseModel):
    volunteer_id: int
    top_n: Optional[int] = 3

class AIRecommendRequest(BaseModel):
    volunteer_skills: List[str]
    location: str
    availability: str

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = ""

# ─── Routes ──────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "VolunteerConnect API is running 🚀", "version": "1.0.0"}

@app.get("/volunteers")
def get_volunteers():
    return {"volunteers": volunteers_db, "count": len(volunteers_db)}

@app.get("/events")
def get_events():
    return {"events": events_db, "count": len(events_db)}

@app.get("/impact")
def get_impact():
    return {"impact": impact_data}

@app.post("/match")
def match_volunteer_to_events(req: MatchRequest):
    volunteer = next((v for v in volunteers_db if v["id"] == req.volunteer_id), None)
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")

    scored = []
    for event in events_db:
        skill_overlap = len(set(volunteer["skills"]) & set(event["required_skills"]))
        location_bonus = 2 if volunteer["location"] == event["location"] else 0
        score = skill_overlap * 3 + location_bonus + (1 if event["slots"] - event["registered"] > 2 else 0)
        if score > 0:
            scored.append({**event, "match_score": score, "skill_overlap": list(set(volunteer["skills"]) & set(event["required_skills"]))})

    scored.sort(key=lambda x: x["match_score"], reverse=True)
    return {"volunteer": volunteer, "matches": scored[:req.top_n]}

@app.post("/ai/recommend")
async def ai_recommend(req: AIRecommendRequest):
    prompt = f"""You are a smart volunteer coordinator assistant for India.
A volunteer has the following profile:
- Skills: {', '.join(req.volunteer_skills)}
- Location: {req.location}
- Availability: {req.availability}

Suggest 3 impactful social events or roles this volunteer should join.
For each, give: Event Name, Why it fits, Expected Impact.
Keep it concise and motivating. Format as JSON array with keys: event_name, reason, impact."""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Clean up markdown code fences if present
        text = text.replace("```json", "").replace("```", "").strip()
        recommendations = json.loads(text)
    except Exception as e:
        recommendations = [
            {"event_name": "Community Teaching Drive", "reason": "Matches your teaching skills", "impact": "Educate 50+ students"},
            {"event_name": "Digital Literacy Workshop", "reason": "Tech skills can help rural youth", "impact": "Bridge digital divide"},
            {"event_name": "Mentorship Program", "reason": "Your experience guides newcomers", "impact": "Shape 10+ careers"},
        ]

    return {"recommendations": recommendations}

@app.post("/ai/chat")
async def ai_chat(req: ChatRequest):
    system = """You are VolunteerConnect's AI assistant. Help volunteers find opportunities,
understand their impact, and stay motivated. Be warm, concise, and action-oriented.
This platform connects volunteers to social impact events across India."""

    prompt = f"{system}\n\nUser: {req.message}"
    try:
        response = model.generate_content(prompt)
        return {"reply": response.text.strip()}
    except Exception as e:
        return {"reply": "I'm here to help you make a difference! Could you tell me more about your skills or what kind of volunteering you're interested in?"}

@app.get("/analytics")
def get_analytics():
    skill_distribution = {}
    for v in volunteers_db:
        for skill in v["skills"]:
            skill_distribution[skill] = skill_distribution.get(skill, 0) + 1

    return {
        "skill_distribution": skill_distribution,
        "avg_rating": round(sum(v["rating"] for v in volunteers_db) / len(volunteers_db), 2),
        "total_hours_contributed": sum(v["hours_per_week"] * v["past_events"] for v in volunteers_db),
        "events_by_location": {"Pune": 2, "Mumbai": 1, "Bangalore": 1},
        "impact": impact_data,
    }
