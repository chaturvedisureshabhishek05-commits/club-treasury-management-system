from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from controller.csv_manager import CSVManager
from controller.treasury_service import TreasuryService
from model.account import Account


class TreasuryServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.csv = CSVManager(Path(self.temp_dir.name))
        self.csv.save_accounts(
            [
                Account("source", "Sport", Decimal("100.00")),
                Account("target", "Events", Decimal("20.00")),
            ]
        )
        self.service = TreasuryService(self.csv)

    def tearDown(self):
        self.temp_dir.cleanup()

    def balances(self):
        return {account.account_id: account.balance for account in self.service.list_accounts()}

    def test_deposit_is_persisted(self):
        self.service.deposit("source", "25.50")
        self.assertEqual(self.balances()["source"], Decimal("125.50"))

    def test_withdrawal_is_persisted(self):
        self.service.withdraw("source", "30")
        self.assertEqual(self.balances()["source"], Decimal("70.00"))

    def test_transfer_updates_both_accounts(self):
        self.service.transfer("source", "target", "40")
        self.assertEqual(self.balances()["source"], Decimal("60.00"))
        self.assertEqual(self.balances()["target"], Decimal("60.00"))

    def test_overdraft_is_rejected_without_changing_balance(self):
        with self.assertRaisesRegex(ValueError, "Insufficient"):
            self.service.withdraw("source", "100.01")
        self.assertEqual(self.balances()["source"], Decimal("100.00"))

    def test_duplicate_account_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.service.create_account("source", "Other", 10)

    def test_transactions_are_recorded(self):
        self.service.deposit("source", "5")
        transactions = self.csv.load_transactions()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].transaction_type, "deposit")
        self.assertEqual(transactions[0].amount, Decimal("5.00"))


if __name__ == "__main__":
    unittest.main()
