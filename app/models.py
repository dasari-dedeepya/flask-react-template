from app import db
from datetime import datetime

class Task(db.Model):
    """Model representing a task."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    # Relationship: one task has many comments
    comments = db.relationship("Comment", backref="task", cascade="all, delete-orphan")

class Comment(db.Model):
    """Model representing a comment on a task."""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign key: link to the task this comment belongs to
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)
