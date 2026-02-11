from flask import Blueprint, request, jsonify
from flask_login import (
    login_user,
    login_required,
    current_user,
    logout_user,
)
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User, JobApplication, db, ApplicationStatus

main = Blueprint("main", __name__)


# --------------------
# HOME
# --------------------
@main.route("/")
def home():
    return {"message": "Welcome to JobTrackr API"}


# --------------------
# AUTH
# --------------------
@main.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return {"error": "No data provided"}, 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return {"error": "All fields are required"}, 400

    if User.query.filter_by(username=username).first():
        return {"error": "Username already exists"}, 400

    if User.query.filter_by(email=email).first():
        return {"error": "Email already exists"}, 400

    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return {"message": "User registered successfully"}, 201


@main.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return {"error": "No data provided"}, 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"error": "Email and password required"}, 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return {"error": "Invalid credentials"}, 401


    access_token = create_access_token(identity=str(user.id))

    return {"message": "Login successful", "access_token": access_token}, 200


@main.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    logout_user()
    return {"message": "Logged out successfully"}, 200


# --------------------
# DASHBOARD
# --------------------
@main.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    # FIX: convert back to int
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    return {
        "message": "Welcome to your dashboard",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        },
    }


# --------------------
# CREATE APPLICATION
# --------------------
@main.route("/applications", methods=["POST"])
@jwt_required()
def create_application():
    data = request.get_json()

    if not data:
        return {"error": "No data provided"}, 400

    company_name = data.get("company_name")
    position_title = data.get("position_title")

    if not company_name or not position_title:
        return {"error": "company_name and position_title are required"}, 400

    location = data.get("location")
    notes = data.get("notes")
    status_str = data.get("status", "Applied")

    try:
        status = ApplicationStatus(status_str)
    except ValueError:
        return {
            "error": "Invalid status",
            "allowed": [s.value for s in ApplicationStatus],
        }, 400

    # convert identity to int
    user_id = int(get_jwt_identity())

    application = JobApplication(
        user_id=user_id,
        company_name=company_name,
        position_title=position_title,
        location=location,
        notes=notes,
        status=status,
    )

    db.session.add(application)
    db.session.commit()

    return {
        "message": "Application created successfully",
        "application": {
            "id": application.id,
            "company_name": application.company_name,
            "position_title": application.position_title,
            "location": application.location,
            "status": application.status.value,
            "notes": application.notes,
            "date_applied": application.date_applied.isoformat(),
        },
    }, 201


# --------------------
# LIST APPLICATIONS
# --------------------
@main.route("/applications", methods=["GET"])
@jwt_required()
def list_applications():
    #  convert identity to int
    user_id = int(get_jwt_identity())
    applications = JobApplication.query.filter_by(user_id=user_id).all()

    return [
        {
            "id": app.id,
            "company_name": app.company_name,
            "position_title": app.position_title,
            "location": app.location,
            "status": app.status.value,
            "date_applied": app.date_applied.isoformat(),
            "notes": app.notes,
        }
        for app in applications
    ], 200


# --------------------
# UPDATE APPLICATION
# --------------------
@main.route("/applications/<int:app_id>", methods=["PUT"])
@jwt_required()
def update_application(app_id):
    user_id = int(get_jwt_identity())

    application = JobApplication.query.filter_by(
        id=app_id, user_id=user_id
    ).first()

    if not application:
        return {"error": "Application not found"}, 404

    data = request.get_json()

    if "company_name" in data:
        application.company_name = data["company_name"]
    if "position_title" in data:
        application.position_title = data["position_title"]
    if "location" in data:
        application.location = data["location"]
    if "notes" in data:
        application.notes = data["notes"]
    if "status" in data:
        try:
            application.status = ApplicationStatus(data["status"])
        except ValueError:
            return {
                "error": "Invalid status",
                "allowed": [s.value for s in ApplicationStatus],
            }, 400

    db.session.commit()

    return {
        "message": "Application updated successfully",
        "application": {
            "id": application.id,
            "company_name": application.company_name,
            "position_title": application.position_title,
            "location": application.location,
            "status": application.status.value,
            "notes": application.notes,
            "date_applied": application.date_applied.isoformat(),
        },
    }, 200


# --------------------
# DELETE APPLICATION
# --------------------
@main.route("/applications/<int:app_id>", methods=["DELETE"])
@jwt_required()
def delete_application(app_id):
    user_id = int(get_jwt_identity())

    application = JobApplication.query.filter_by(
        id=app_id, user_id=user_id
    ).first()

    if not application:
        return {"error": "Application not found"}, 404

    db.session.delete(application)
    db.session.commit()

    return {"message": "Application deleted successfully"}, 200
