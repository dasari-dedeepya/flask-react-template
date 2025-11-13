import json
import pytest
from app import create_app, db
from app.models import Task, Comment

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Create a dummy task
            task = Task(title="Test Task")
            db.session.add(task)
            db.session.commit()
        yield client

def test_add_comment(client):
    response = client.post(
        "/api/tasks/1/comments",
        data=json.dumps({"content": "First comment"}),
        content_type="application/json",
    )
    assert response.status_code == 201
    assert b"Comment added" in response.data

def test_get_comments(client):
    # Add a comment first
    client.post(
        "/api/tasks/1/comments",
        data=json.dumps({"content": "Another comment"}),
        content_type="application/json",
    )
    response = client.get("/api/tasks/1/comments")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) >= 1

def test_edit_comment(client):
    # Add a comment
    post_response = client.post(
        "/api/tasks/1/comments",
        data=json.dumps({"content": "Edit me"}),
        content_type="application/json",
    )
    comment_id = json.loads(post_response.data)["id"]
    # Edit it
    response = client.put(
        f"/api/comments/{comment_id}",
        data=json.dumps({"content": "Edited content"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert b"Comment updated" in response.data

def test_delete_comment(client):
    # Add a comment
    post_response = client.post(
        "/api/tasks/1/comments",
        data=json.dumps({"content": "Delete me"}),
        content_type="application/json",
    )
    comment_id = json.loads(post_response.data)["id"]
    # Delete it
    response = client.delete(f"/api/comments/{comment_id}")
    assert response.status_code == 200
    assert b"Comment deleted" in response.data
