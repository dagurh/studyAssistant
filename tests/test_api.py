import sys
import os

# Add the root directory to sys.path so `main.py` can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestAPI:

    def test_get_valid_data(self):
        """Test GET request with valid input"""
        response = client.get("/items/1?q=hello")  # Replace with your actual GET endpoint
        assert response.status_code == 200
        assert response.json() == {"item_id":1,"q":"hello"} # Adjust based on your response structure

    def test_get_invalid_data(self):
        """Test GET request with invalid input"""
        response = client.get("/items/1?q=hi")  # Modify based on your params
        assert response.status_code == 422  # Expecting a 400 Bad Request or other error

    # def test_put_valid_data(self):
    #     """Test PUT request with valid input"""
    #     data = {
    #         "field1": "valid_value",
    #         "field2": 123
    #     }
    #     response = client.put("/your-put-endpoint", json=data)  # Modify with your actual PUT endpoint
    #     assert response.status_code == 200
    #     assert response.json()["message"] == "Success"  # Adjust based on your expected response

    # def test_put_invalid_data(self):
    #     """Test PUT request with invalid input"""
    #     data = {
    #         "field1": "",  # Invalid value (empty)
    #         "field2": "wrong_type"  # Should be an integer
    #     }
    #     response = client.put("/your-put-endpoint", json=data)
    #     assert response.status_code == 422  # Expecting validation error

