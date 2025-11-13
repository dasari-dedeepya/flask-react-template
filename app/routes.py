from flask import Blueprint, request, jsonify
from .models import db, Comment

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/tasks/<int:task_id>/comments', methods=['POST'])
def add_comment(task_id):
    data = request.get_json()
    content = data.get('content')

    comment = Comment(content=content, task_id=task_id)
    db.session.add(comment)
    db.session.commit()

    return jsonify({'message': 'Comment added', 'id': comment.id, 'content': comment.content}), 201

@comments_bp.route('/tasks/<int:task_id>/comments', methods=['GET'])
def get_comments(task_id):
    comments = Comment.query.filter_by(task_id=task_id).all()
    return jsonify([{'id': c.id, 'content': c.content} for c in comments])

@comments_bp.route('/comments/<int:id>', methods=['PUT'])
def edit_comment(id):
    data = request.get_json()
    comment = Comment.query.get(id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    comment.content = data.get('content', comment.content)
    db.session.commit()
    return jsonify({'message': 'Comment updated', 'content': comment.content})

@comments_bp.route('/comments/<int:id>', methods=['DELETE'])
def delete_comment(id):
    comment = Comment.query.get(id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted'})


