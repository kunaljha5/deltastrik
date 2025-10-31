"""
Chat log view for DeltaStrik's terminal UI.
Displays user and AI messages in a scrollable, auto-updating panel.
"""

from textual.containers import VerticalScroll
from textual.widgets import Static
from textual.reactive import reactive
from textual import events
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich.console import Group
from typing import Any
from typing import Union


class ChatView(VerticalScroll):
    """
    A scrollable chat display area that renders user and assistant messages.
    """

    messages: Any = reactive(list)

    def on_mount(self):
        """Called when the widget is mounted."""
        self.can_focus = True  # Enable focus for keyboard scrolling
        # Create a static widget to hold content
        self.content_widget = Static("")
        self.mount(self.content_widget)

    def add_message(self, role: str, content: str):
        """Add a message and refresh."""
        new_messages = self.messages.copy()
        new_messages.append((role, content))
        self.messages = new_messages

    async def watch_messages(self, _):
        """Automatically scroll to bottom whenever new messages appear."""
        # Update content widget
        if hasattr(self, 'content_widget'):
            self.content_widget.update(self._render_messages())
            # Use multiple scroll attempts with delays to handle large content rendering
            self.set_timer(0.05, self._scroll_to_bottom)
            self.set_timer(0.15, self._scroll_to_bottom)

    def _scroll_to_bottom(self):
        """Helper to scroll to bottom."""
        self.scroll_end(animate=False)

    async def on_key(self, event: events.Key) -> None:
        """Handle keyboard scrolling events."""
        if event.key == "up":
            self.scroll_up(animate=True)
            event.prevent_default()
        elif event.key == "down":
            self.scroll_down(animate=True)
            event.prevent_default()
        elif event.key == "pageup":
            self.scroll_page_up(animate=True)
            event.prevent_default()
        elif event.key == "pagedown":
            self.scroll_page_down(animate=True)
            event.prevent_default()
        elif event.key == "home":
            self.scroll_home(animate=True)
            event.prevent_default()
        elif event.key == "end":
            self.scroll_end(animate=True)
            event.prevent_default()

    def _render_messages(self):
        """Render chat messages using Rich components."""
        rendered: list[Union[Panel, Text]] = []
        for i, (role, content) in enumerate(self.messages):
            body: Union[Text, Markdown]
            if role == "user":
                header = Text("You:", style="bold cyan")
                body = Text.from_markup(content)
                rendered.append(Panel(body, title=header, border_style="cyan", expand=False))

            elif role == "system":
                header = Text("System:", style="bold yellow")
                body = Text.from_markup(content)
                rendered.append(Panel(body, title=header, border_style="yellow", expand=False))

            else:  # assistant
                header = Text("DeltaStrik:", style="bold green")
                try:
                    body = Markdown(content)
                except Exception:
                    body = Text.from_markup(content)
                rendered.append(Panel(body, title=header, border_style="green", expand=False))

            # Add spacing between messages (except after the last one)
            if i < len(self.messages) - 1:
                rendered.append(Text(""))

        return Group(*rendered) if rendered else Text("")
