"""Entry point for the club treasury management system."""

from gui.login_view import LoginView


def main() -> None:
    LoginView().run()


if __name__ == "__main__":
    main()

