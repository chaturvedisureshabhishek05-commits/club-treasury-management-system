"""Login window and role-based navigation."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from controller.auth_manager import AuthManager


class LoginView:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Club Treasury System - Login")
        self.root.resizable(False, False)
        self.auth = AuthManager()

        tk.Label(self.root, text="Username:").grid(row=0, column=0, padx=10, pady=6, sticky="e")
        self.username_entry = tk.Entry(self.root, width=28)
        self.username_entry.grid(row=0, column=1, padx=10, pady=6)
        tk.Label(self.root, text="Password:").grid(row=1, column=0, padx=10, pady=6, sticky="e")
        self.password_entry = tk.Entry(self.root, width=28, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=6)
        tk.Button(self.root, text="Login", command=self.authenticate).grid(
            row=2, column=0, columnspan=2, pady=10
        )
        self.root.bind("<Return>", lambda _event: self.authenticate())

    def authenticate(self) -> None:
        user = self.auth.authenticate(
            self.username_entry.get(),
            self.password_entry.get(),
        )
        if user is None:
            messagebox.showerror("Login failed", "Invalid username or password.")
            return
        self.root.destroy()
        self.open_role_specific_view(user.role)

    @staticmethod
    def open_role_specific_view(role: str) -> None:
        if role == "Admin":
            from gui.admin_view import AdminView

            AdminView()
        elif role == "Kassenwart":
            from gui.kassenwart_view import KassenwartView

            KassenwartView()
        elif role == "Referentin-Finanzen":
            from gui.finance_view import FinanceView

            FinanceView()
        else:
            messagebox.showerror("Role error", f"Unsupported role: {role}")

    def run(self) -> None:
        self.username_entry.focus_set()
        self.root.mainloop()

