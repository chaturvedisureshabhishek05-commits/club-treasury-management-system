# Club Treasury Management System

A desktop Python application for managing departmental club accounts through a role-based Tkinter interface. Account, user and transaction data are persisted in CSV files so the project can be run without external dependencies or a database server.

This project was originally developed as a university group project by **Xiong and Suresh Abhishek Chaturvedi**. The public portfolio version was cleaned and completed with persistent transactions, safer demo-password storage, tests and updated project documentation.

## Features

- role-based login for administrators, cashiers and finance reviewers;
- creation of departmental accounts;
- deposits, withdrawals and transfers with validation;
- prevention of negative balances;
- persistent account and transaction records using CSV files;
- account overview and aggregated financial summary;
- PBKDF2-hashed demo passwords instead of plaintext credentials;
- modular separation of GUI, controller/service, model and data layers.

## Technical structure

- `gui/` — Tkinter interfaces for login and the three user roles
- `controller/` — authentication, CSV persistence and treasury operations
- `model/` — account, user and transaction models
- `data/` — demonstration users, accounts and transaction history
- `docs/` — original German documentation and UML diagrams
- `tests/` — automated tests for authentication and financial operations

## Run the application

Python 3.10 or newer is recommended. The application uses only Python's standard library.

```bash
python main.py
```

### Demo users

| Role | Username | Password |
| --- | --- | --- |
| Administrator | `admin` | `admin123` |
| Cashier | `cashier` | `cashier123` |
| Finance reviewer | `finance` | `finance123` |

The credentials are demonstration data for local use only. This educational prototype is not intended for production financial data.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## Documentation

- [Project documentation (German)](docs/Dokumentation.pdf)
- [User manual (German)](docs/Benutzerhandbuch.pdf)
- [Class diagram](docs/class_diagram.png)
- [State diagram](docs/state_diagram.png)
- [Use-case diagram](docs/use_case_diagram.png)

## What the project demonstrates

The project demonstrates object-oriented Python, role-based workflows, GUI development with Tkinter, CSV persistence, validation of financial operations, password verification and automated testing. It also shows how a larger problem can be divided into models, controllers and presentation components.

