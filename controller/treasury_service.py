"""Business rules for club-account operations."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation

from controller.csv_manager import CSVManager
from model.account import Account
from model.transaction import Transaction


class TreasuryService:
    def __init__(self, csv_manager: CSVManager | None = None) -> None:
        self.csv = csv_manager or CSVManager()

    def list_accounts(self) -> list[Account]:
        return self.csv.load_accounts()

    def create_account(self, account_id: str, department: str, balance=0) -> Account:
        clean_id = account_id.strip()
        clean_department = department.strip()
        if not clean_id or not clean_department:
            raise ValueError("Account ID and department are required.")
        accounts = self.csv.load_accounts()
        if any(account.account_id == clean_id for account in accounts):
            raise ValueError("An account with this ID already exists.")
        amount = self._positive_or_zero(balance)
        account = Account(clean_id, clean_department, amount)
        accounts.append(account)
        self.csv.save_accounts(accounts)
        return account

    def deposit(self, account_id: str, amount) -> Transaction:
        accounts = self.csv.load_accounts()
        account = self._find(accounts, account_id)
        value = self._positive(amount)
        account.deposit(value)
        transaction = Transaction.create("deposit", value, target_account=account.account_id)
        self._persist(accounts, transaction)
        return transaction

    def withdraw(self, account_id: str, amount) -> Transaction:
        accounts = self.csv.load_accounts()
        account = self._find(accounts, account_id)
        value = self._positive(amount)
        account.withdraw(value)
        transaction = Transaction.create("withdrawal", value, source_account=account.account_id)
        self._persist(accounts, transaction)
        return transaction

    def transfer(self, source_id: str, target_id: str, amount) -> Transaction:
        if source_id.strip() == target_id.strip():
            raise ValueError("Source and target accounts must be different.")
        accounts = self.csv.load_accounts()
        source = self._find(accounts, source_id)
        target = self._find(accounts, target_id)
        value = self._positive(amount)
        source.withdraw(value)
        target.deposit(value)
        transaction = Transaction.create(
            "transfer",
            value,
            source_account=source.account_id,
            target_account=target.account_id,
        )
        self._persist(accounts, transaction)
        return transaction

    def summary(self) -> tuple[int, Decimal]:
        accounts = self.csv.load_accounts()
        return len(accounts), sum((account.balance for account in accounts), Decimal("0.00"))

    def _persist(self, accounts: list[Account], transaction: Transaction) -> None:
        self.csv.save_accounts(accounts)
        self.csv.append_transaction(transaction)

    @staticmethod
    def _find(accounts: list[Account], account_id: str) -> Account:
        clean_id = account_id.strip()
        for account in accounts:
            if account.account_id == clean_id:
                return account
        raise ValueError(f"Account '{clean_id}' was not found.")

    @staticmethod
    def _positive(amount) -> Decimal:
        value = TreasuryService._decimal(amount)
        if value <= 0:
            raise ValueError("Amount must be greater than zero.")
        return value

    @staticmethod
    def _positive_or_zero(amount) -> Decimal:
        value = TreasuryService._decimal(amount)
        if value < 0:
            raise ValueError("Initial balance cannot be negative.")
        return value

    @staticmethod
    def _decimal(amount) -> Decimal:
        try:
            return Decimal(str(amount)).quantize(Decimal("0.01"))
        except (InvalidOperation, TypeError):
            raise ValueError("Amount must be a valid number.") from None

