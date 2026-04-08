from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from backend.app.main import app


class TestAPI(unittest.TestCase):
	def setUp(self) -> None:
		self.client = TestClient(app)

	def test_health_endpoint(self) -> None:
		response = self.client.get("/health")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(), {"status": "ok"})

	def test_analyze_endpoint(self) -> None:
		response = self.client.post(
			"/analyze",
			json={"text": "The proliferation of complex systems can significantly impact modern education."},
		)
		self.assertEqual(response.status_code, 200)
		payload = response.json()
		self.assertIn(payload["level"], {"A1", "A2", "B1", "B2", "C1", "C2"})
		self.assertIn("simplified_text", payload)
		self.assertIn("difficult_words", payload)


if __name__ == "__main__":
	unittest.main()

