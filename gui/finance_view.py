"""Read-only finance overview."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from controller.treasury_service import TreasuryService


class FinanceView:
    def __init__(self) -> None:
        self.service = TreasuryService()
        self.root = tk.Tk()
        self.root.title("Club Treasury - Finance Overview")
        tk.Button(self.root, text="View all accounts", width=28, command=self.view_all_accounts).pack(
            padx=25, pady=8
        )
        tk.Button(self.root, text="View financial summary", width=28, command=self.view_summary).pack(
            padx=25, pady=8
        )
        self.root.mainloop()

    def view_all_accounts(self) -> None:
        accounts = self.service.list_accounts()
        if not accounts:
            messagebox.showinfo("Accounts", "No accounts are available.", parent=self.root)
            return
        lines = ["Account ID | Department | Balance"]
        lines.extend(
            f"{account.account_id} | {account.department} | {account.balance:.2f} EUR"
            for account in accounts
        )
        messagebox.showinfo("Accounts", "\n".join(lines), parent=self.root)

    def view_summary(self) -> None:
        count, total = self.service.summary()
        messagebox.showinfo(
            "Financial summary",
            f"Number of accounts: {count}\nTotal balance: {total:.2f} EUR",
            parent=self.root,
        )

