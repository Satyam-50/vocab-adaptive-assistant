from __future__ import annotations

import unittest

from backend.app.api.dependencies import get_adaptive_service


class TestServices(unittest.TestCase):
	def test_adaptive_service_analyze(self) -> None:
		service = get_adaptive_service()
		result = service.analyze("The proliferation of complex systems can significantly impact modern education.")

		self.assertIn(result.level, {"A1", "A2", "B1", "B2", "C1", "C2"})
		self.assertTrue(result.simplified_text)
		self.assertGreaterEqual(len(result.difficult_words), 1)


if __name__ == "__main__":
	unittest.main()

