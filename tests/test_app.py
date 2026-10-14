import tempfile
import unittest
from pathlib import Path
from app import create_app

class StudyPlannerWebTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.app = create_app({
            "TESTING": True,
            "SECRET_KEY": "test",
            "DATABASE": str(Path(self.temp_dir.name) / "test.db"),
        })
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_home_page_renders_empty_state(self):
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        self.assertIn(b"No tasks yet", response.data)

    def test_add_task_and_render_it(self):
        response = self.client.post("/tasks", data={
            "title": "Review recursion", "course": "CSI2510",
            "due_date": "2026-11-01", "estimated_minutes": "45"
        }, follow_redirects=True)
        self.assertEqual(200, response.status_code)
        self.assertIn(b"Review recursion", response.data)
        self.assertIn(b"CSI2510", response.data)

    def test_invalid_task_is_not_saved(self):
        response = self.client.post("/tasks", data={
            "title": "", "course": "CSI2510",
            "due_date": "2026-11-01", "estimated_minutes": "45"
        }, follow_redirects=True)
        self.assertIn(b"Task title and course are required", response.data)
        self.assertIn(b"No tasks yet", response.data)

    def test_complete_and_delete_task(self):
        self.client.post("/tasks", data={
            "title": "Finish lab", "course": "CHM1711",
            "due_date": "2026-11-02", "estimated_minutes": "30"
        })
        with self.app.test_client() as client:
            page = client.get("/")
            # Task ID starts at 1 in the fresh test database.
            self.assertIn(b"Finish lab", page.data)
            response = client.post("/tasks/1/complete", follow_redirects=True)
            self.assertIn(b"Completed", response.data)
            response = client.post("/tasks/1/delete", follow_redirects=True)
            self.assertNotIn(b"Finish lab", response.data)

if __name__ == "__main__":
    unittest.main()
