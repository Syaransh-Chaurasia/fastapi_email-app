import unittest

from app.main import app


class TestAppSmoke(unittest.TestCase):
    def test_core_routes_registered(self):
        paths = {route.path for route in app.routes}
        self.assertIn("/", paths)
        self.assertIn("/register", paths)
        self.assertIn("/login", paths)


if __name__ == "__main__":
    unittest.main()
