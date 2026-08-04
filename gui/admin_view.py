"""Administrator interface for account creation."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, simpledialog

from controller.treasury_service import TreasuryService


class AdminView:
    def __init__(self) -> None:
        self.service = TreasuryService()
        self.root = tk.Tk()
        self.root.title("Club Treasury - Administration")
        tk.Button(self.root, text="Create account", command=self.create_account).pack(
            padx=25, pady=25
        )
        self.root.mainloop()

    def create_account(self) -> None:
        account_id = simpledialog.askstring("Create account", "Account ID:", parent=self.root)
        department = simpledialog.askstring("Create account", "Department:", parent=self.root)
        initial_balance = simpledialog.askfloat(
            "Create account", "Initial balance:", parent=self.root, minvalue=0.0
        )
        if account_id is None or department is None or initial_balance is None:
            return
        try:
            account = self.service.create_account(account_id, department, initial_balance)
        except ValueError as error:
            messagebox.showerror("Cannot create account", str(error), parent=self.root)
            return
        messagebox.showinfo(
            "Account created",
            f"Account {account.account_id} was created for {account.department}.",
            parent=self.root,
        )

