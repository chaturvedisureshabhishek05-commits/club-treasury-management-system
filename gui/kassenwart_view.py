"""Cashier interface for deposits, withdrawals and transfers."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, simpledialog

from controller.treasury_service import TreasuryService


class KassenwartView:
    def __init__(self) -> None:
        self.service = TreasuryService()
        self.root = tk.Tk()
        self.root.title("Club Treasury - Transactions")
        for label, command in (
            ("Deposit", self.deposit),
            ("Withdraw", self.withdraw),
            ("Transfer", self.transfer),
        ):
            tk.Button(self.root, text=label, width=24, command=command).pack(padx=25, pady=6)
        self.root.mainloop()

    def deposit(self) -> None:
        account_id = simpledialog.askstring("Deposit", "Account ID:", parent=self.root)
        amount = simpledialog.askfloat("Deposit", "Amount:", parent=self.root, minvalue=0.01)
        if account_id is None or amount is None:
            return
        self._execute(self.service.deposit, account_id, amount, success="Deposit saved.")

    def withdraw(self) -> None:
        account_id = simpledialog.askstring("Withdraw", "Account ID:", parent=self.root)
        amount = simpledialog.askfloat("Withdraw", "Amount:", parent=self.root, minvalue=0.01)
        if account_id is None or amount is None:
            return
        self._execute(self.service.withdraw, account_id, amount, success="Withdrawal saved.")

    def transfer(self) -> None:
        source = simpledialog.askstring("Transfer", "Source account ID:", parent=self.root)
        target = simpledialog.askstring("Transfer", "Target account ID:", parent=self.root)
        amount = simpledialog.askfloat("Transfer", "Amount:", parent=self.root, minvalue=0.01)
        if source is None or target is None or amount is None:
            return
        self._execute(self.service.transfer, source, target, amount, success="Transfer saved.")

    def _execute(self, operation, *args, success: str) -> None:
        try:
            operation(*args)
        except ValueError as error:
            messagebox.showerror("Transaction failed", str(error), parent=self.root)
            return
        messagebox.showinfo("Success", success, parent=self.root)

