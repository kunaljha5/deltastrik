# deltastrik/tui/input_bar.py
"""
User input widget for DeltaStrik.
Handles keyboard input and emits an event when the user presses Enter.
"""

from textual.widgets import Input
from textual.message import Message


class InputSubmitted(Message):
    """Custom message fired when the user submits text."""
    def __init__(self, sender, text: str) -> None:
        super().__init__()
        self.sender = sender
        self.text = text


# class InputBar(Input):
#     """A custom single-line input bar for user messages."""
#
#     def __init__(self, placeholder: str = "Type your message...", **kwargs):
#         super().__init__(placeholder=placeholder, **kwargs)
#
#     def on_key(self, event):
#         """Handle key events for Enter and Escape.on_input_submitted"""
#         if event.key == "enter":
#             text = self.value.strip()
#             if text:
#                 self.post_message(InputSubmitted(self, text))
#                 self.value = ""  # clear after sending
#         elif event.key == "escape":
#             self.value = ""

class InputBar(Input):
    """Single-line input for chat messages."""
    def __init__(self):
        super().__init__(placeholder="Type your message here...")