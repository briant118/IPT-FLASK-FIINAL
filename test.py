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
        self.assertEqual(response.data.decode(), "<p> hello ceianyy</p>")

    def test_get_branch(self):
        response = self.app.get("/branch")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Robinson" in response.data.decode())

    def test_get_branch_id(self):
        response = self.app.get("/branch/001")
        self.assertEqual(response.status_code, 200)
        
        self.assertTrue("Malvar" in response.data.decode())
        


if __name__ == "__main__":
    unittest.main()
