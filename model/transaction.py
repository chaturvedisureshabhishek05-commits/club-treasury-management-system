"""Persisted financial transaction model."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4


@dataclass(frozen=True)
class Transaction:
    transaction_id: str
    transaction_type: str
    amount: Decimal
    timestamp: str
    source_account: str = ""
    target_account: str = ""

    @classmethod
    def create(
        cls,
        transaction_type: str,
        amount: Decimal,
        *,
        source_account: str = "",
        target_account: str = "",
    ) -> "Transaction":
        return cls(
            uuid4().hex,
            transaction_type,
            amount.quantize(Decimal("0.01")),
            datetime.now(timezone.utc).isoformat(timespec="seconds"),
            source_account,
            target_account,
        )

    @staticmethod
    def fieldnames() -> list[str]:
        return [
            "transaction_id",
            "transaction_type",
            "amount",
            "timestamp",
            "source_account",
            "target_account",
        ]

    def to_row(self) -> dict[str, str]:
        return {
            "transaction_id": self.transaction_id,
            "transaction_type": self.transaction_type,
            "amount": f"{self.amount:.2f}",
            "timestamp": self.timestamp,
            "source_account": self.source_account,
            "target_account": self.target_account,
        }

    @classmethod
    def from_row(cls, row: dict[str, str]) -> "Transaction":
        return cls(
            row["transaction_id"],
            row["transaction_type"],
            Decimal(row["amount"]),
            row["timestamp"],
            row.get("source_account", ""),
            row.get("target_account", ""),
        )

