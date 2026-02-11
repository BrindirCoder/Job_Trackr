from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import enum

db = SQLAlchemy()


class ApplicationStatus(enum.Enum):
    APPLIED = "Applied"
    INTERVIEW = "Interview"
    OFFER = "Offer"
    REJECTED = "Rejected"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship("JobApplication", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    position_title = db.Column(db.String(100), nullable=False)
    status = db.Column(
        db.Enum(ApplicationStatus),
        default=ApplicationStatus.APPLIED,
        nullable=False,
    )
    location = db.Column(db.String(100))
    date_applied = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
