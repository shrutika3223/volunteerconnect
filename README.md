# 🤝 VolunteerConnect
### Data-Driven Volunteer Coordination for Social Impact
**Google Solution Challenge 2026 | Team TechMinds**

---

## 🌟 Problem Statement
Volunteer coordination is fragmented — NGOs struggle to find the right volunteers for events, and volunteers have no centralized way to discover impactful opportunities matching their skills and location. This results in wasted potential, low engagement, and poor social impact.

## 💡 Solution
**VolunteerConnect** is an AI-powered platform that uses **Google Gemini** to intelligently match volunteers to social impact events based on skills, location, and availability. It provides real-time analytics, personalized AI recommendations, and a conversational assistant for volunteers.

---

## 🚀 Features
- 🤖 **AI-Powered Matching** — Skill + location-based volunteer ↔ event matching
- ✨ **Gemini Recommendations** — Personalized event suggestions via Gemini 1.5 Flash
- 💬 **AI Chat Assistant** — Volunteer guidance chatbot powered by Gemini
- 📊 **Impact Analytics** — Real-time dashboards with charts
- 📅 **Event Management** — Browse, filter, and register for events
- 👤 **Volunteer Directory** — Profiles with skills, ratings, history

---

## 🛠️ Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Frontend  | React 18, Recharts, Lucide React    |
| Backend   | FastAPI (Python 3.11+)              |
| AI        | Google Gemini 1.5 Flash API         |
| Deployment| Google Cloud Run + Firebase Hosting |

---

## 📁 Project Structure
```
volunteerconnect/
├── backend/
│   ├── main.py           # FastAPI app + all routes
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── App.js
    │   ├── App.css
    │   ├── index.js
    │   ├── services/
    │   │   └── api.js
    │   └── pages/
    │       ├── Dashboard.js
    │       ├── Volunteers.js
    │       ├── Events.js
    │       ├── AIAssistant.js
    │       └── Analytics.js
    └── package.json
```

---

## ⚙️ Setup & Run

### Prerequisites
- Python 3.11+
- Node.js 18+
- Google Gemini API Key → https://aistudio.google.com/

### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Add your GEMINI_API_KEY in .env
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm start
```
Open http://localhost:3000

### API Docs
Visit http://localhost:8000/docs for interactive Swagger UI.

---

## 🔑 Environment Variables
```
GEMINI_API_KEY=your_google_gemini_api_key
```
Get your key at: https://aistudio.google.com/app/apikey

---

## ☁️ Cloud Deployment (Google Cloud)
```bash
# Backend → Cloud Run
gcloud run deploy volunteerconnect-api \
  --source ./backend \
  --set-env-vars GEMINI_API_KEY=your_key \
  --allow-unauthenticated

# Frontend → Firebase Hosting
npm run build
firebase deploy
```

---

## 👥 Team TechMinds
- **Team Leader:** Shrutika Kadam
- Google Solution Challenge 2026

---

## 📌 Links
- GitHub: _your-repo-link_
- Demo Video: _your-demo-link_
- Live MVP: _your-deployment-link_
