"""Role-based authentication service."""

from __future__ import annotations

from controller.csv_manager import CSVManager
from controller.passwords import verify_password
from model.user import User


class AuthManager:
    def __init__(self, csv_manager: CSVManager | None = None) -> None:
        self.csv = csv_manager or CSVManager()

    def authenticate(self, username: str, password: str) -> User | None:
        normalized_username = username.strip()
        for user in self.csv.load_users():
            if (
                user.username == normalized_username
                and verify_password(password, user.password_hash)
            ):
                return user
        return None

