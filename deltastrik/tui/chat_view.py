"""
Chat log view for DeltaStrik's terminal UI.
Displays user and AI messages in a scrollable panel.
"""

from textual.widget import Widget
from textual.reactive import reactive
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich.console import Group


class ChatView(Widget):
    """
    A scrollable chat display area that renders user and assistant messages.
    Compatible across Textual versions.
    """

    messages = reactive(list)

    def on_mount(self):
        """Called when the widget is mounted."""
        self.refresh()

    def add_message(self, role: str, content: str):
        """Add a message and refresh."""
        new_messages = self.messages.copy()
        new_messages.append((role, content))
        self.messages = new_messages
        self.refresh()

    def render(self):
        """Render chat messages using Rich components."""
        rendered = []
        for role, content in self.messages:
            if role == "user":
                header = Text("You:", style="bold cyan")
                body = Text(content)
                rendered.append(Panel(body, title=header, border_style="cyan", expand=False))
            else:
                header = Text("DeltaStrik:", style="bold green")
                try:
                    body = Markdown(content)
                except Exception:
                    body = Text(content)
                rendered.append(Panel(body, title=header, border_style="green", expand=False))

        # ✅ Group is the correct way to combine multiple renderables in Rich
        return Group(*rendered)
