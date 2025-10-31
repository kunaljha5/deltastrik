# deltastrik/tui/input_bar.py
"""
User input widget for DeltaStrik.
Handles keyboard input and emits an event when the user presses Enter.
Supports command history navigation with up/down arrow keys.
"""

from textual.widgets import Input
from textual import events


class InputBar(Input):
    """
    Single-line input for chat messages with command history support.
    Use Up/Down arrows to navigate through previous commands.
    """

    def __init__(self, max_history: int = 100):
        super().__init__(placeholder="Type your message here...")
        self.command_history: list[str] = []  # Stores previous commands
        self.history_index: int = -1  # Current position in history (-1 = not browsing)
        self.current_draft: str = ""  # Preserves what user is typing
        self.max_history = max_history

    def add_to_history(self, command: str) -> None:
        """
        Add a command to the history.
        Skips empty commands and consecutive duplicates.
        """
        command = command.strip()
        if not command:
            return

        # Don't add if it's the same as the last command
        if self.command_history and self.command_history[-1] == command:
            return

        self.command_history.append(command)

        # Limit history size
        if len(self.command_history) > self.max_history:
            self.command_history.pop(0)

        # Reset history navigation
        self.history_index = -1
        self.current_draft = ""

    async def on_key(self, event: events.Key) -> None:
        """Handle up/down arrow keys for command history navigation."""

        if event.key == "up":
            # Navigate to older command
            event.prevent_default()
            self._navigate_history_up()

        elif event.key == "down":
            # Navigate to newer command
            event.prevent_default()
            self._navigate_history_down()

        elif event.key == "escape":
            # If input has text, clear it; otherwise propagate to switch focus
            if self.value.strip():
                self.value = ""
                self.history_index = -1
                self.current_draft = ""
                event.prevent_default()
            # else: let the event propagate to App for focus switching

    def _navigate_history_up(self) -> None:
        """Navigate to the previous (older) command in history."""
        if not self.command_history:
            return

        # First time pressing up: save current draft
        if self.history_index == -1:
            self.current_draft = self.value
            self.history_index = len(self.command_history)

        # Move to older command
        if self.history_index > 0:
            self.history_index -= 1
            self.value = self.command_history[self.history_index]
            self.cursor_position = len(self.value)

    def _navigate_history_down(self) -> None:
        """Navigate to the next (newer) command in history."""
        if not self.command_history or self.history_index == -1:
            return

        # Move to newer command
        self.history_index += 1

        if self.history_index >= len(self.command_history):
            # Reached the end: restore current draft
            self.value = self.current_draft
            self.history_index = -1
            self.current_draft = ""
        else:
            self.value = self.command_history[self.history_index]

        self.cursor_position = len(self.value)

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission - clear the input field."""
        # Note: The actual command processing happens in app.py
        # This just clears the field after submission
        self.value = ""
        self.history_index = -1
        self.current_draft = ""
