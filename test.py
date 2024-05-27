import unittest
from main import app
import warnings


class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Welcome</p>")

    def test_get_branch(self):
        # Mock login
        with self.app.session_transaction() as sess:
            sess['username'] = 'Bryan'

        response = self.app.get("/branch")
        self.assertEqual(response.status_code, 200)

    def test_get_branch_id(self):
        # Mock login
        with self.app.session_transaction() as sess:
            sess['username'] = 'Bryan'

        response = self.app.get("/branch/1")
        self.assertEqual(response.status_code, 200)

    def test_add_branch(self):
        # Mock login
        with self.app.session_transaction() as sess:
            sess['username'] = 'Bryan'

        response = self.app.post("/branch", json={
            "Branch_Location": "New Location",
            "Branch_Name": "New Name",
            "Total_Sales": 1000
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Branch added successfully", response.data.decode())

    def test_update_branch(self):
        # Mock login
        with self.app.session_transaction() as sess:
            sess['username'] = 'Bryan'

        response = self.app.put("/branch/1", json={
            "Branch_Location": "Updated Location",
            "Branch_Name": "Updated Name",
            "Total_Sales": 2000
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Branch updated successfully", response.data.decode())

    def test_delete_branch(self):
        # Mock login
        with self.app.session_transaction() as sess:
            sess['username'] = 'Bryan'

        response = self.app.delete("/branch/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Branch deleted successfully", response.data.decode())


if __name__ == "__main__":
    unittest.main()
