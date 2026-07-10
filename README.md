# MedAssist AI — Enterprise AI Medical Assistant
### Powered by IBM watsonx Orchestrate

A production-ready, full-stack AI Medical Assistant web application built with **Python Flask** and **IBM watsonx Orchestrate**.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd medassist
pip install -r requirements.txt
```

### 2. Configure IBM watsonx API
```bash
# Copy the example environment file
cp env.example .env

# Edit .env and add your keys
WATSONX_API_KEY=your_actual_api_key_here
WATSONX_PROJECT_ID=your_actual_project_id_here
```

### 3. Run the Application
```bash
python app.py
```

Then open **http://localhost:5000** in your browser.

---

## 📁 Project Structure

```
medassist/
├── app.py              # Flask application entry point
├── routes.py           # All URL routes and API endpoints
├── services.py         # IBM watsonx Orchestrate integration + AGENT_INSTRUCTIONS
├── utils.py            # File handling, text processing, validation helpers
├── config.py           # Environment-based configuration
├── requirements.txt    # Python dependencies
├── env.example         # Environment variable template (copy to .env)
├── medassist.log       # Application log file (auto-created)
├── uploads/            # Uploaded medical reports (auto-created)
├── templates/
│   ├── base.html       # Base layout with sidebar, topbar, dark mode
│   ├── index.html      # Landing page
│   ├── chat.html       # AI Chat Assistant
│   ├── dashboard.html  # Health Dashboard
│   ├── symptoms.html   # Symptom Checker
│   ├── diseases.html   # Disease Information Library
│   ├── medications.html# Medication Information
│   ├── reports.html    # Medical Report Upload & Analysis
│   ├── timeline.html   # Health History Timeline
│   ├── appointments.html # Appointment Reminders
│   ├── settings.html   # Application Settings
│   ├── about.html      # About Page
│   ├── login.html      # Login
│   ├── register.html   # Registration
│   ├── profile.html    # User Profile
│   ├── notifications.html # Notification Center
│   ├── feedback.html   # Feedback Form
│   ├── contact.html    # Contact Page
│   └── errors/
│       ├── 404.html    # Not Found error page
│       └── 500.html    # Server Error page
└── static/
    ├── css/
    │   └── main.css    # Complete design system stylesheet
    └── js/
        └── main.js     # All frontend logic (Theme, Chat, API, etc.)
```

---

## 🤖 Customizing the AI Agent

All AI agent behavior is configured in **`services.py`** inside the clearly marked `AGENT_INSTRUCTIONS` section:

```python
# ============================================================
# AGENT INSTRUCTIONS — Customize AI Behavior Here
# ============================================================

AGENT_PERSONA = "..."          # AI personality and communication style
AGENT_EXPERTISE = [...]        # Topics the AI covers
AGENT_SAFETY_RULES = [...]     # Safety rules (always enforced)
AGENT_RESPONSE_FORMAT = "..."  # How responses are structured
AGENT_DISCLAIMER = "..."       # Medical disclaimer appended to responses
AGENT_SYSTEM_PROMPT = "..."    # Full system prompt sent to watsonx

AGENT_MODEL_PARAMS = {         # Model generation parameters
    "decoding_method": "greedy",
    "max_new_tokens": 1024,
    "temperature": 0.7,
    ...
}
```

---

## 🔗 REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/chat` | Send message, get AI response |
| `POST` | `/api/symptoms` | Analyze symptoms |
| `POST` | `/api/disease` | Get disease information |
| `POST` | `/api/medication` | Get medication information |
| `POST` | `/api/report/upload` | Upload & analyze medical report |
| `GET`  | `/api/health-tip` | Get daily health tip |
| `POST` | `/api/wellness-plan` | Generate wellness plan |

### Chat Example
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the symptoms of type 2 diabetes?"}'
```

---

## 🔒 Security Notes

- API keys are stored **only** in `.env` and never exposed to the frontend
- File uploads are sanitized with Werkzeug's `secure_filename`
- User input is sanitized via `utils.sanitize_input()` 
- The `.env` file is git-ignored by default
- CORS is restricted to `/api/*` endpoints only
- Maximum file upload size is 16MB

---

## 🎨 UI Features

- ✅ Light / Dark mode (Ctrl+D to toggle)
- ✅ Glassmorphism effects on hero, auth pages
- ✅ Animated gradient backgrounds
- ✅ Skeleton loading states
- ✅ Toast notifications
- ✅ Responsive sidebar (collapsible)
- ✅ Smooth animations and transitions
- ✅ Fully responsive (mobile/tablet/desktop)
- ✅ Keyboard shortcuts (Ctrl+K search, Ctrl+D dark mode)
- ✅ Voice input and text-to-speech output
- ✅ Chat export

---

## ⚠️ Medical Disclaimer

**MedAssist AI is for educational purposes only.** It does not provide medical diagnoses or replace professional healthcare. Always consult qualified healthcare professionals for personal medical decisions. In emergencies, call local emergency services (911 or equivalent).

---

## 🛠 Built With

- **Backend:** Python 3.10+, Flask 3.0, Flask-CORS
- **AI Engine:** IBM watsonx Orchestrate (Granite 13B)
- **Frontend:** HTML5, CSS3, Bootstrap 5, Vanilla JS
- **File Processing:** PyPDF2, python-docx
- **Environment:** python-dotenv
