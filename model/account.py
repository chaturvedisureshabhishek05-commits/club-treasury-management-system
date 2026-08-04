"""Departmental account model."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Account:
    account_id: str
    department: str
    balance: Decimal = Decimal("0.00")

    def deposit(self, amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError("Deposit must be greater than zero.")
        self.balance = (self.balance + amount).quantize(Decimal("0.01"))

    def withdraw(self, amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal must be greater than zero.")
        if self.balance < amount:
            raise ValueError("Insufficient account balance.")
        self.balance = (self.balance - amount).quantize(Decimal("0.01"))

    def to_row(self) -> dict[str, str]:
        return {
            "account_id": self.account_id,
            "department": self.department,
            "balance": f"{self.balance:.2f}",
        }

    @classmethod
    def from_row(cls, row: dict[str, str]) -> "Account":
        return cls(
            row["account_id"].strip(),
            row["department"].strip(),
            Decimal(row["balance"].strip()).quantize(Decimal("0.01")),
        )

