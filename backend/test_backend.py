import unittest
from flask_testing import TestCase
from backend import app  # Replace 'your_flask_app_filename' with the name of your Python file
import json
import os

class TestFlaskApi(TestCase):
    @classmethod
    def create_app(cls):
        app.config['TESTING'] = True
        return app

    @classmethod
    def setUpClass(cls):
        # Ensuring the in_progress directory exists and creating a jobtalk.json file in it
        if not os.path.exists("in_progress"):
            os.makedirs("in_progress")
        with open("in_progress/jobtalk.json", 'w') as f:
            json.dump({"status": "in_progress"}, f)
    @classmethod
    def tearDownClass(cls):
        # Clean up the in_progress directory
        for filename in os.listdir("in_progress"):
            os.remove(os.path.join("in_progress", filename))

    def test_get_all_analysis(self):
        response = self.client.get('/get_all_analysis')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        expected_keys = ["AntSimulator", "dbeaver", "glide", "glide-transformations", "gson", "hurl", "jobtalk"]
        for key in expected_keys:
            self.assertIn(key, data)
            if key == "glide-transformations":
                self.assertEqual(len(data[key]),3)
        self.assertIn("in_progress", data["jobtalk"])

    def test_get_analysis_existing_file(self):
        response = self.client.get('/get_analysis/dbeaver/2024-05-04')
        self.assertEqual(response.status_code, 200)
        # Check some content if you know what should be in this file
        data = json.loads(response.data)
        self.assertIn('issues', data)  # Replace 'some_expected_key' with an actual key from the JSON file

    def test_get_analysis_non_existing_file(self):
        response = self.client.get('/get_analysis/nonexistent_repo/2024-05-05')
        self.assertEqual(response.status_code, 404)

    def test_create_analysis_already_in_progress(self):
        response = self.client.post('/create_analysis', json={'repo_url': 'https://github.com/some_repo'})
        self.assertEqual(response.status_code, 400)
        self.assertIn("already in progress", json.loads(response.data)["error"])

    def test_create_analysis_allowed(self):
        for filename in os.listdir("in_progress"):
            os.remove(f"in_progress/{filename}")
        response = self.client.post('/create_analysis', json={'repo_url': 'https://github.com/new_repo'})
        self.assertEqual(response.status_code, 202)
        self.assertIn("successfully", json.loads(response.data)["message"])
        for filename in os.listdir("in_progress"):
            self.assertEqual(filename, "new_repo.json")

    
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestFlaskApi('test_get_all_analysis'))
    suite.addTest(TestFlaskApi('test_get_analysis_existing_file'))
    suite.addTest(TestFlaskApi('test_get_analysis_non_existing_file'))
    suite.addTest(TestFlaskApi('test_create_analysis_already_in_progress'))
    suite.addTest(TestFlaskApi('test_create_analysis_allowed'))
    runner = unittest.TextTestRunner()
    runner.run(suite)