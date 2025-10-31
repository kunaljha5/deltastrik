# deltastrik/tui/status_bar.py
"""
Status bar widget for DeltaStrik.
Displays model name, connection status, and latency.
"""

from datetime import datetime
from textual.widget import Widget
from textual.reactive import reactive
from rich.text import Text
from deltastrik.core.config import load_config

model_config = load_config()

class StatusBar(Widget):
    """
    Displays model name, connection status, and latency.
    """

    model_name: str = reactive(model_config.get("model"))
    connection_status: str = reactive(model_config.get("connection_status"))
    status: str = reactive("Ready")         # e.g. "Ready", "Thinking", "Error"
    latency_ms: int | None = reactive(None) # e.g. 320

    def render(self) -> Text:
        """
        Called automatically by Textual when any reactive property changes.
        """
        # Build parts
        parts = [
            f"Model: {self.model_name}",
            f"Status: {self.status}",
        ]

        if self.latency_ms is not None:
            parts.append(f"Latency: {self.latency_ms} ms")

        # Timestamp for freshness
        ts = datetime.now().strftime("%H:%M:%S")
        parts.append(f"⏱ {ts}")

        # Format as styled Rich text
        text = " | ".join(parts)
        style = "bold green" if self.status.lower() == "ready" else "bold yellow"
        if "error" in self.status.lower():
            style = "bold red"

        return Text(text, style=style, justify="center")

    # convenience methods
    def update_status(self, status: str, latency_ms: int | None = None):
        """Update the displayed status and optional latency."""
        self.status = status
        if latency_ms is not None:
            self.latency_ms = latency_ms
        self.refresh()
