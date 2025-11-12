from flask import Blueprint, request, jsonify
from app import db
from app.models import Task, Comment

# Create a blueprint for comment routes
comments_bp = Blueprint("comments", __name__, url_prefix="/api/comments")

# -----------------------
# GET: all comments for a task
# -----------------------
@comments_bp.route("/<int:task_id>", methods=["GET"])
def get_comments(task_id):
    comments = Comment.query.filter_by(task_id=task_id).all()
    return jsonify([
        {
            "id": c.id,
            "content": c.content,
            "created_at": c.created_at,
            "updated_at": c.updated_at,
        } for c in comments
    ]), 200

# -----------------------
# POST: add a new comment to a task
# -----------------------
@comments_bp.route("/<int:task_id>", methods=["POST"])
def add_comment(task_id):
    data = request.get_json()
    if not data or not data.get("content"):
        return jsonify({"error": "Content is required"}), 400

    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    new_comment = Comment(content=data["content"], task_id=task_id)
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({
        "id": new_comment.id,
        "content": new_comment.content,
        "created_at": new_comment.created_at
    }), 201

# -----------------------
# PUT: edit a comment
# -----------------------
@comments_bp.route("/<int:comment_id>", methods=["PUT"])
def edit_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    data = request.get_json()
    if not data or not data.get("content"):
        return jsonify({"error": "Content is required"}), 400

    comment.content = data["content"]
    db.session.commit()

    return jsonify({
        "id": comment.id,
        "content": comment.content,
        "updated_at": comment.updated_at
    }), 200

# -----------------------
# DELETE: delete a comment
# -----------------------
@comments_bp.route("/<int:comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Comment deleted successfully"}), 200
