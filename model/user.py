"""Authenticated application user."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    username: str
    password_hash: str
    role: str

    def to_row(self) -> dict[str, str]:
        return {
            "username": self.username,
            "password_hash": self.password_hash,
            "role": self.role,
        }

    @classmethod
    def from_row(cls, row: dict[str, str]) -> "User":
        return cls(
            row["username"].strip(),
            row["password_hash"].strip(),
            row["role"].strip(),
        )

