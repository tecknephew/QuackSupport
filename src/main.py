import logging
import sys

from PyQt6.QtWidgets import QApplication

from .anthropic import AnthropicClient
from .store import Store
from .window import MainWindow

logging.basicConfig(
    filename="agent.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def main():
    app = QApplication(sys.argv)

    app.setQuitOnLastWindowClosed(
        False
    )  # Prevent app from quitting when window is closed

    store = Store()
    anthropic_client = AnthropicClient()

    window = MainWindow(store, anthropic_client)
    window.show()  # Just show normally, no maximize

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
