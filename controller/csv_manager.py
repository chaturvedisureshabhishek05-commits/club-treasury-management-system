"""CSV persistence for users, accounts and transactions."""

from __future__ import annotations

import csv
from pathlib import Path

from model.account import Account
from model.transaction import Transaction
from model.user import User


class CSVManager:
    def __init__(self, data_dir: str | Path | None = None) -> None:
        project_root = Path(__file__).resolve().parents[1]
        self.data_dir = Path(data_dir) if data_dir else project_root / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.users_file = self.data_dir / "users.csv"
        self.accounts_file = self.data_dir / "accounts.csv"
        self.transactions_file = self.data_dir / "transactions.csv"

    def load_users(self) -> list[User]:
        if not self.users_file.exists():
            return []
        with self.users_file.open("r", newline="", encoding="utf-8") as handle:
            return [
                User.from_row(row)
                for row in csv.DictReader(handle)
                if row.get("username") and row.get("password_hash") and row.get("role")
            ]

    def save_users(self, users: list[User]) -> None:
        self._write_rows(
            self.users_file,
            ["username", "password_hash", "role"],
            [user.to_row() for user in users],
        )

    def load_accounts(self) -> list[Account]:
        if not self.accounts_file.exists():
            return []
        with self.accounts_file.open("r", newline="", encoding="utf-8") as handle:
            accounts: list[Account] = []
            for row in csv.DictReader(handle):
                try:
                    accounts.append(Account.from_row(row))
                except (KeyError, ValueError):
                    continue
            return accounts

    def save_accounts(self, accounts: list[Account]) -> None:
        self._write_rows(
            self.accounts_file,
            ["account_id", "department", "balance"],
            [account.to_row() for account in accounts],
        )

    def load_transactions(self) -> list[Transaction]:
        if not self.transactions_file.exists():
            return []
        with self.transactions_file.open("r", newline="", encoding="utf-8") as handle:
            return [Transaction.from_row(row) for row in csv.DictReader(handle)]

    def append_transaction(self, transaction: Transaction) -> None:
        exists = self.transactions_file.exists() and self.transactions_file.stat().st_size > 0
        with self.transactions_file.open("a", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=Transaction.fieldnames(),
            )
            if not exists:
                writer.writeheader()
            writer.writerow(transaction.to_row())

    @staticmethod
    def _write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

