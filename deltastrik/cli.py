# deltastrik/cli.py

# import sys
from deltastrik.tui.app import DeltaStrikApp
from deltastrik.core.config import load_config


def main() -> None:
    """Main entrypoint for the deltastrik CLI."""
    config = load_config()
    app = DeltaStrikApp(config)
    app.run()  # start the TUI
