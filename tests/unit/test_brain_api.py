"""
K.A.O.S. Unit Tests - Brain API Module
Tests for Flask API endpoints and request handling
"""

import unittest
import json
from backend.src.brain.app.main import app


class TestBrainAPI(unittest.TestCase):
    """Test suite for Brain Flask API"""

    def setUp(self):
        """Initialize test client"""
        self.app = app
        self.client = self.app.test_client()
        self.app.config["TESTING"] = True

    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get("/api/v1/health")
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertIn("status", data)
        self.assertEqual(data["status"], "healthy")

    def test_analyze_endpoint_valid_input(self):
        """Test analyze endpoint with valid input"""
        payload = {"command": "nmap -sV localhost", "session_id": "test-001"}
        response = self.client.post(
            "/api/v1/analyze",
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("heuristic_layer", data)

    def test_analyze_endpoint_missing_input(self):
        """Test analyze endpoint with missing required fields"""
        payload = {"session_id": "test-001"}  # Missing 'command'
        response = self.client.post(
            "/api/v1/analyze",
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_analyze_endpoint_destructive_command(self):
        """Test detection of destructive command"""
        payload = {
            "command": "rm -rf /",
            "session_id": "test-002",
        }
        response = self.client.post(
            "/api/v1/analyze",
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        risk_level = data.get("heuristic_layer", {}).get("risk_level")
        self.assertEqual(risk_level, "CRITICAL")


if __name__ == "__main__":
    unittest.main()
