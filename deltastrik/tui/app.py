# deltastrik/tui/app.py
"""
Reactive TUI application for DeltaStrik.
Uses Textual to provide a structured chat-like terminal UI.
"""

import time
import asyncio
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual import events
from deltastrik.tui.chat_view import ChatView
from deltastrik.tui.input_bar import InputBar
from deltastrik.tui.status_bar import StatusBar
from deltastrik.core.session_manager import SessionManager
from deltastrik.core.ollama_client import OllamaClient
from deltastrik.core.prompt_engine import build_system_prompt
from deltastrik.core.command_handler import CommandHandler
from textual.widgets import Input


class DeltaStrikApp(App):
    """Textual-powered chat interface for DeltaStrik."""

    CSS_PATH = "deltastrik.tcss"  # Path to Textual CSS

    # Keybindings for the app
    BINDINGS = [
        ("ctrl+m", "toggle_mouse", "Toggle Mouse Capture"),
    ]

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.session = SessionManager(config=self.config)
        self.client = OllamaClient(config)
        self.system_prompt = build_system_prompt(config)
        self.command_handler = CommandHandler(
            self.session,
            self.client,
            build_system_prompt,
            app=self,
        )
        self.mouse_capture_enabled = True

    def compose(self) -> ComposeResult:
        """Declare the TUI layout."""
        self.chat_view = ChatView()
        self.input_bar = InputBar()
        self.status_bar = StatusBar()

        with Vertical(id="main-layout"):
            yield self.chat_view
            yield self.input_bar
            yield self.status_bar

    async def on_mount(self) -> None:
        """Set initial focus on the input bar when app starts."""
        self.input_bar.focus()
        # Show initial hint about copying
        self.status_bar.update_status("Ready • Hold Shift to select/copy text")

    def action_toggle_mouse(self) -> None:
        """Show information about text copying."""
        help_message = """[bold cyan]How to copy text from DeltaStrik:[/bold cyan]

[bold]Method 1:[/bold] Hold [yellow]Shift[/yellow] key while selecting text with your mouse
  • Works in most modern terminals (iTerm2, Terminal.app, Windows Terminal, etc.)
  • Bypasses mouse capture temporarily

[bold]Method 2:[/bold] Use your terminal's keyboard shortcuts
  • macOS: Cmd+C after selecting with Shift held
  • Linux/Windows: Ctrl+Shift+C or right-click menu

[bold]Method 3:[/bold] Use terminal-specific features
  • iTerm2: Cmd+Option+drag to select
  • tmux: Enter copy mode with prefix + [

[bold]Tip:[/bold] If Shift doesn't work, check your terminal's settings for mouse capture bypass keys."""

        self.chat_view.add_message("system", help_message)
        self.status_bar.update_status("Check chat for copy instructions")

    async def on_key(self, event: events.Key) -> None:
        """Handle global key bindings for focus management."""
        # Press Escape to focus chat view for scrolling
        if event.key == "escape":
            if self.chat_view.has_focus:
                # If already in chat view, return to input
                self.input_bar.focus()
            else:
                # Switch to chat view for scrolling
                self.chat_view.focus()
            event.prevent_default()
            event.stop()

    async def on_input_submitted(self, event: Input.Submitted):
        """Handle new user messages."""
        user_text = event.value.strip()
        if not user_text:
            return

        # Add to command history
        self.input_bar.add_to_history(user_text)

        command_response = self.command_handler.handle(user_text)
        if command_response:
            self.chat_view.add_message("system", command_response)
            return
        # Display user message
        self.chat_view.add_message("user", user_text)
        # Show processing indicator
        self.chat_view.add_processing_indicator()
        self.status_bar.update_status("Thinking...")

        # Yield to event loop to allow UI to update before blocking API call
        await asyncio.sleep(0.01)

        start = time.time()
        try:
            # Run the blocking HTTP call in a background thread to keep UI responsive
            response = await asyncio.to_thread(
                self.client.query,
                prompt=self.system_prompt,
                user_message=user_text,
                history=self.session.history,
            )

            self.session.add_user_message(user_text)
            self.session.add_assistant_message(response)
            latency = int((time.time() - start) * 1000)

            # Remove processing indicator before showing response
            self.chat_view.remove_processing_indicator()
            self.chat_view.add_message("assistant", response)
            self.status_bar.update_status("Ready", latency)

        except Exception as e:
            # Remove processing indicator before showing error
            self.chat_view.remove_processing_indicator()
            self.chat_view.add_message("assistant", f"[red]Error:[/red] {e}")
            self.status_bar.update_status("Error")


if __name__ == "__main__":
    from deltastrik.core.config import load_config

    config = load_config()
    DeltaStrikApp(config).run()
