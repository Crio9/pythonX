import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from task_app import database
from task_app.main import app


class TaskAPITest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        db_path = Path(self.directory.name) / "test.db"
        self.engine = create_engine(
            f"sqlite:///{db_path}", connect_args={"check_same_thread": False}
        )
        self.engine_patch = patch.object(database, "engine", self.engine)
        self.session_patch = patch.object(
            database, "SessionLocal", sessionmaker(bind=self.engine)
        )
        self.engine_patch.start()
        self.session_patch.start()
        self.client = TestClient(app)
        self.client.__enter__()

    def tearDown(self):
        self.client.__exit__(None, None, None)
        self.session_patch.stop()
        self.engine_patch.stop()
        self.engine.dispose()
        self.directory.cleanup()

    def create_task(self, title="Learn SQL", priority=3):
        response = self.client.post(
            "/tasks", json={"title": title, "priority": priority}
        )
        self.assertEqual(response.status_code, 201, response.text)
        return response.json()

    def test_empty_collection(self):
        response = self.client.get("/tasks")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_full_crud(self):
        task = self.create_task()
        task_id = task["id"]
        self.assertIsInstance(task_id, int)
        self.assertEqual(task["title"], "Learn SQL")

        response = self.client.get(f"/tasks/{task_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), task)
        self.assertEqual(self.client.get("/tasks").json(), [task])

        updated = {"title": "Submit homework", "priority": 1}
        response = self.client.put(f"/tasks/{task_id}", json=updated)
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json(), {"id": task_id, **updated})
        self.assertEqual(self.client.get(f"/tasks/{task_id}").json(), response.json())

        response = self.client.delete(f"/tasks/{task_id}")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertEqual(self.client.get(f"/tasks/{task_id}").status_code, 404)
        self.assertEqual(self.client.get("/tasks").json(), [])

    def test_missing_task_returns_404(self):
        for method in ("get", "put", "delete"):
            with self.subTest(method=method):
                kwargs = {"json": {"title": "Missing"}} if method == "put" else {}
                response = self.client.request(method, "/tasks/999", **kwargs)
                self.assertEqual(response.status_code, 404)
                self.assertEqual(response.json(), {"detail": "Task not found"})

    def test_invalid_data_returns_422_and_does_not_change_task(self):
        task = self.create_task()
        invalid_bodies = [
            {},
            {"title": ""},
            {"title": "   "},
            {"title": "x" * 101},
            {"title": None},
            {"title": "Valid", "priority": 0},
            {"title": "Valid", "priority": 6},
            {"title": "Valid", "priority": None},
            {"title": "Valid", "priority": "high"},
            {"title": "Valid", "id": 999},
        ]
        for body in invalid_bodies:
            for method, path in (("post", "/tasks"), ("put", f"/tasks/{task['id']}")):
                with self.subTest(body=body, method=method):
                    response = self.client.request(method, path, json=body)
                    self.assertEqual(response.status_code, 422, response.text)
        self.assertEqual(self.client.get("/tasks").json(), [task])

    def test_default_priority_and_whitespace(self):
        response = self.client.post("/tasks", json={"title": "  Learn SQL  "})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "Learn SQL")
        self.assertEqual(response.json()["priority"], 3)

    def test_update_and_delete_only_affect_selected_task(self):
        first = self.create_task("First")
        second = self.create_task("Second")
        third = self.create_task("Third")
        response = self.client.put(
            f"/tasks/{second['id']}", json={"title": "Changed", "priority": 5}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get(f"/tasks/{first['id']}").json(), first)
        self.assertEqual(self.client.get(f"/tasks/{third['id']}").json(), third)
        self.assertEqual(self.client.delete(f"/tasks/{second['id']}").status_code, 204)
        fourth = self.create_task("Fourth")
        tasks = self.client.get("/tasks").json()
        self.assertEqual(tasks, [first, third, fourth])
        self.assertEqual(len({task["id"] for task in tasks}), 3)

    def test_changes_survive_restart(self):
        kept = self.create_task("Before restart")
        removed = self.create_task("To delete")
        updated = {"title": "After update", "priority": 2}
        self.assertEqual(
            self.client.put(f"/tasks/{kept['id']}", json=updated).status_code, 200
        )
        self.assertEqual(self.client.delete(f"/tasks/{removed['id']}").status_code, 204)

        self.client.__exit__(None, None, None)
        self.engine.dispose()
        self.client = TestClient(app)
        self.client.__enter__()

        self.assertEqual(
            self.client.get("/tasks").json(), [{"id": kept["id"], **updated}]
        )
        self.assertEqual(self.client.get(f"/tasks/{removed['id']}").status_code, 404)


if __name__ == "__main__":
    unittest.main()
