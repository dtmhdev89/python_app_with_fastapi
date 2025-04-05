from todoapp.main import app
from todoapp.routers.todos import get_db, get_current_user
from fastapi import status
from todoapp.models import Todos
import todoapp.test.utils as test_utils
from todoapp.test.utils import test_todo


app.dependency_overrides[get_db] = test_utils.override_get_db
app.dependency_overrides[get_current_user] = test_utils.override_get_current_user


def test_read_all_authenticated(test_todo):
    response = test_utils.client.get("/")

    assert response.status_code == status.HTTP_200_OK, "Should return status code of 200"
    assert response.json() == [
        {
            "id": 1,
            "title": "Learn to code",
            "description": "desc",
            "priority": 5,
            "complete": False,
            "owner_id": 1
        }
    ]


def test_read_one_authenticated(test_todo):
    response = test_utils.client.get("/todos/1")

    assert response.status_code == status.HTTP_200_OK, "Should return status code of 200"
    assert response.json() == {
            "id": 1,
            "title": "Learn to code",
            "description": "desc",
            "priority": 5,
            "complete": False,
            "owner_id": 1
        }


def test_read_one_authenticated_not_found():
    response = test_utils.client.get("/todos/1")

    assert response.status_code == status.HTTP_404_NOT_FOUND, "Should return status code of 404"
    assert response.json() == {'detail': 'Todo not found'}


def test_create_todo(test_todo):
    request_data = {
        'title': "new todo creation",
        'description': 'todo desc',
        'priority': 5,
        'complete': False,
        'owner_id': 1
    }

    response = test_utils.client.post("/todos", json=request_data)

    assert response.status_code == status.HTTP_201_CREATED

    db = test_utils.TestingSessionLocal()
    todo_count = db.query(Todos).filter(Todos.owner_id == 1).count()
    model = db.query(Todos).filter(Todos.owner_id == 1)\
        .filter(Todos.id != test_todo.id).first()

    assert todo_count == 2
    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")


def test_update_todo(test_todo):
    request_data = {
        'title': "update existed todo",
        'description': 'todo desc',
        'priority': 5,
        'complete': False,
    }

    response = test_utils.client.put(f"/todos/{test_todo.id}", json=request_data)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    db = test_utils.TestingSessionLocal()
    todo_count = db.query(Todos).filter(Todos.owner_id == 1).count()
    todo = db.query(Todos).filter(Todos.id == test_todo.id).first()
    
    assert todo_count == 1
    assert todo.title == request_data.get("title")
    assert todo.description == request_data.get("description")
    assert todo.priority == request_data.get("priority")
    assert todo.complete is False


def test_update_todo_not_found(test_todo):
    request_data = {
        'title': "update existed todo",
        'description': 'todo desc',
        'priority': 5,
        'complete': False,
    }

    response = test_utils.client.put("/todos/9999", json=request_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo(test_todo):
    response = test_utils.client.delete(f"/todos/{test_todo.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = test_utils.TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == test_todo.id).first()

    assert model is None


def test_delete_todo_not_found():
    response = test_utils.client.delete("/todos/9999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}
