from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from controller.auth_manager import AuthManager
from controller.csv_manager import CSVManager
from controller.passwords import hash_password
from model.user import User


class AuthenticationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.csv = CSVManager(Path(self.temp_dir.name))
        self.csv.save_users(
            [User("tester", hash_password("secret", salt="test-salt"), "Admin")]
        )
        self.auth = AuthManager(self.csv)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_valid_credentials_return_user(self):
        user = self.auth.authenticate("tester", "secret")
        self.assertIsNotNone(user)
        self.assertEqual(user.role, "Admin")

    def test_invalid_password_is_rejected(self):
        self.assertIsNone(self.auth.authenticate("tester", "wrong"))


if __name__ == "__main__":
    unittest.main()

