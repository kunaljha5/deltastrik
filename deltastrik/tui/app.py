# deltastrik/tui/app.py
"""
Reactive TUI application for DeltaStrik.
Uses Textual to provide a structured chat-like terminal UI.
"""

import time
from textual.app import App, ComposeResult
from textual.containers import Vertical
from deltastrik.tui.chat_view import ChatView
from deltastrik.tui.input_bar import InputBar
from deltastrik.tui.status_bar import StatusBar
from deltastrik.core.session_manager import SessionManager
from deltastrik.core.ollama_client import OllamaClient
from deltastrik.core.prompt_engine import build_system_prompt
from textual.widgets import Input


class DeltaStrikApp(App):
    """Textual-powered chat interface for DeltaStrik."""

    CSS_PATH = "deltastrik.tcss"  # Path to Textual CSS

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.session = SessionManager()
        self.client = OllamaClient(config)
        self.system_prompt = build_system_prompt(config)

    def compose(self) -> ComposeResult:
        """Declare the TUI layout."""
        self.chat_view = ChatView()
        self.input_bar = InputBar()
        self.status_bar = StatusBar()

        with Vertical(id="main-layout"):
            yield self.chat_view
            yield self.input_bar
            yield self.status_bar

    async def on_input_submitted(self, event: Input.Submitted):
        """Handle new user messages."""
        user_text = event.value.strip()
        if not user_text:
            return

        # Display user message
        self.chat_view.add_message("user", user_text)
        self.status_bar.update_status("Thinking...")

        start = time.time()
        try:
            response = self.client.query(
                prompt=self.system_prompt,
                user_message=user_text,
                history=self.session.history,
            )

            self.session.add_user_message(user_text)
            self.session.add_assistant_message(response)
            latency = int((time.time() - start) * 1000)

            self.chat_view.add_message("assistant", response)
            self.status_bar.update_status("Ready", latency)

        except Exception as e:
            self.chat_view.add_message("assistant", f"[red]Error:[/red] {e}")
            self.status_bar.update_status("Error")


if __name__ == "__main__":
    from deltastrik.core.config import load_config

    config = load_config()
    DeltaStrikApp(config).run()
