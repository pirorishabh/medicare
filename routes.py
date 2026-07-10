"""
routes.py — Flask API Route Definitions
=========================================
All REST API endpoints and page rendering routes.
"""

import logging
from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from services import watsonx
from utils import (
    sanitize_input, save_upload, extract_text_from_file,
    validate_json_body, success_response, error_response,
    markdown_to_html_safe,
)

logger = logging.getLogger(__name__)

main_bp = Blueprint("main", __name__)
api_bp = Blueprint("api", __name__, url_prefix="/api")


# ══════════════════════════════════════════════════════════════
# PAGE ROUTES
# ══════════════════════════════════════════════════════════════

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/chat")
def chat():
    return render_template("chat.html")

@main_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@main_bp.route("/symptoms")
def symptoms():
    return render_template("symptoms.html")

@main_bp.route("/diseases")
def diseases():
    return render_template("diseases.html")

@main_bp.route("/medications")
def medications():
    return render_template("medications.html")

@main_bp.route("/reports")
def reports():
    return render_template("reports.html")

@main_bp.route("/timeline")
def timeline():
    return render_template("timeline.html")

@main_bp.route("/appointments")
def appointments():
    return render_template("appointments.html")

@main_bp.route("/settings")
def settings():
    return render_template("settings.html")

@main_bp.route("/about")
def about():
    return render_template("about.html")

@main_bp.route("/login")
def login():
    return render_template("login.html")

@main_bp.route("/register")
def register():
    return render_template("register.html")

@main_bp.route("/profile")
def profile():
    return render_template("profile.html")

@main_bp.route("/notifications")
def notifications():
    return render_template("notifications.html")

@main_bp.route("/feedback")
def feedback():
    return render_template("feedback.html")

@main_bp.route("/contact")
def contact():
    return render_template("contact.html")


# ══════════════════════════════════════════════════════════════
# API ROUTES — AI Features
# ══════════════════════════════════════════════════════════════

@api_bp.route("/chat", methods=["POST"])
def api_chat():
    """Main chat endpoint — sends message to IBM watsonx and returns AI response."""
    data = request.get_json(silent=True) or {}
    valid, err = validate_json_body(data, ["message"])
    if not valid:
        return error_response(err)

    message = sanitize_input(data["message"])
    history = data.get("history", [])

    # Sanitize history entries
    safe_history = [
        {"role": h.get("role", "user"), "content": sanitize_input(h.get("content", ""))}
        for h in history[-10:]
    ]

    result = watsonx.chat(message, safe_history)
    return success_response({
        "message": result["text"],
        "model": result.get("agent_id", result.get("model_id", "")),
        "tokens": result.get("output_tokens", 0),
        "demo": result.get("demo", False),
    })


@api_bp.route("/symptoms", methods=["POST"])
def api_symptoms():
    """Symptom checker endpoint."""
    data = request.get_json(silent=True) or {}
    valid, err = validate_json_body(data, ["symptoms"])
    if not valid:
        return error_response(err)

    symptoms = sanitize_input(data["symptoms"])
    result = watsonx.check_symptoms(symptoms)
    return success_response({"analysis": result["text"], "demo": result.get("demo", False)})


@api_bp.route("/disease", methods=["POST"])
def api_disease():
    """Disease information endpoint."""
    data = request.get_json(silent=True) or {}
    valid, err = validate_json_body(data, ["disease"])
    if not valid:
        return error_response(err)

    disease = sanitize_input(data["disease"], max_length=200)
    result = watsonx.get_disease_info(disease)
    return success_response({"info": result["text"], "disease": disease, "demo": result.get("demo", False)})


@api_bp.route("/medication", methods=["POST"])
def api_medication():
    """Medication information endpoint."""
    data = request.get_json(silent=True) or {}
    valid, err = validate_json_body(data, ["medication"])
    if not valid:
        return error_response(err)

    medication = sanitize_input(data["medication"], max_length=200)
    result = watsonx.get_medication_info(medication)
    return success_response({"info": result["text"], "medication": medication, "demo": result.get("demo", False)})


@api_bp.route("/report/upload", methods=["POST"])
def api_report_upload():
    """Medical report upload and AI analysis endpoint."""
    if "file" not in request.files:
        return error_response("No file provided.")

    file = request.files["file"]
    try:
        filename, filepath = save_upload(file)
        text = extract_text_from_file(filepath)

        if not text.strip():
            return error_response("Could not extract text from the uploaded file.")

        result = watsonx.analyze_report(text)
        return success_response({
            "filename": filename,
            "extracted_text": text[:1000],
            "analysis": result["text"],
            "demo": result.get("demo", False),
        })

    except ValueError as e:
        return error_response(str(e))
    except Exception as e:
        logger.exception("Report upload error")
        return error_response("Failed to process the file. Please try again.", 500)


@api_bp.route("/health-tip", methods=["GET"])
def api_health_tip():
    """Daily health tip endpoint."""
    result = watsonx.get_health_tip()
    return success_response({"tip": result["text"], "demo": result.get("demo", False)})


@api_bp.route("/wellness-plan", methods=["POST"])
def api_wellness_plan():
    """Personalized wellness plan endpoint."""
    data = request.get_json(silent=True) or {}
    profile = {
        "age": sanitize_input(str(data.get("age", ""))),
        "gender": sanitize_input(str(data.get("gender", ""))),
        "conditions": sanitize_input(str(data.get("conditions", "none"))),
        "goals": sanitize_input(str(data.get("goals", "general wellness"))),
    }
    result = watsonx.generate_wellness_plan(profile)
    return success_response({"plan": result["text"], "demo": result.get("demo", False)})


# ══════════════════════════════════════════════════════════════
# API ROUTES — Application State
# ══════════════════════════════════════════════════════════════

@api_bp.route("/session/save-chat", methods=["POST"])
def save_chat():
    """Persist chat messages to session storage."""
    data = request.get_json(silent=True) or {}
    if "messages" not in data:
        return error_response("Missing messages.")
    session["chat_history"] = data["messages"][-50:]  # Keep last 50 messages
    return success_response({"saved": True})


@api_bp.route("/session/load-chat", methods=["GET"])
def load_chat():
    """Load chat history from session."""
    return success_response({"messages": session.get("chat_history", [])})


@api_bp.route("/session/clear-chat", methods=["POST"])
def clear_chat():
    """Clear chat session history."""
    session.pop("chat_history", None)
    return success_response({"cleared": True})


# ══════════════════════════════════════════════════════════════
# ERROR HANDLERS
# ══════════════════════════════════════════════════════════════

@main_bp.app_errorhandler(404)
def not_found(e):
    return render_template("errors/404.html"), 404

@main_bp.app_errorhandler(500)
def server_error(e):
    return render_template("errors/500.html"), 500
