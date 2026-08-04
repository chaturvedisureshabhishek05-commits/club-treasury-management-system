"""Password hashing helpers using only Python's standard library."""

from __future__ import annotations

import hashlib
import hmac
import secrets

ALGORITHM = "pbkdf2_sha256"
DEFAULT_ITERATIONS = 120_000


def hash_password(
    password: str,
    *,
    iterations: int = DEFAULT_ITERATIONS,
    salt: str | None = None,
) -> str:
    if not password:
        raise ValueError("Password must not be empty.")
    actual_salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        actual_salt.encode("utf-8"),
        iterations,
    ).hex()
    return f"{ALGORITHM}${iterations}${actual_salt}${digest}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, iterations_text, salt, stored_digest = encoded.split("$", 3)
        if algorithm != ALGORITHM:
            return False
        candidate = hash_password(
            password,
            iterations=int(iterations_text),
            salt=salt,
        ).rsplit("$", 1)[-1]
        return hmac.compare_digest(candidate, stored_digest)
    except (TypeError, ValueError):
        return False

