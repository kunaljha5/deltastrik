# deltastrik/core/session_manager.py
"""
Manages chat sessions and message history for DeltaStrik.
Provides an interface for storing, retrieving, and serializing
conversation context between the user and the LLM (Ollama backend).
"""

from typing import List, Dict, Any
import datetime


class SessionManager:
    """
    Maintains conversation history and context.
    """

    def __init__(self):
        # Chat history follows the typical OpenAI/Ollama format:
        # [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
        self.history: List[Dict[str, str]] = []
        self.created_at: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)

    # ----------------------------------------------------------
    # Message management
    # ----------------------------------------------------------
    def add_user_message(self, message: str):
        """Append a user message to the session."""
        self.history.append({"role": "user", "content": message})

    def add_assistant_message(self, message: str):
        """Append an assistant (model) message to the session."""
        self.history.append({"role": "assistant", "content": message})

    # ----------------------------------------------------------
    # Retrieval & context
    # ----------------------------------------------------------
    def get_recent_context(self, limit: int = 10) -> List[Dict[str, str]]:
        """Return the last N messages for context."""
        return self.history[-limit:]

    @property
    def conversation_length(self) -> int:
        """Total number of messages exchanged."""
        return len(self.history)

    # ----------------------------------------------------------
    # Utility
    # ----------------------------------------------------------
    def reset(self):
        """Clear the chat history for a new session."""
        self.history.clear()

    def export(self) -> Dict[str, Any]:
        """Return session data as a serializable dict."""
        return {
            "created_at": self.created_at.isoformat(),
            "history": self.history,
        }

    # def load_from(self, session_data: Dict[str, Any]):
    #     """Load an existing session from serialized data."""
    #     self.history = session_data.get("history", [])
    #     self.created_at = datetime.datetime.fromisoformat(session_data.get("created_at"))
    def load_from(self, session_data: Dict[str, Any]) -> None:
        """Load an existing session from serialized data."""
        self.history = session_data.get("history", [])

        created_at_raw = session_data.get("created_at")
        if isinstance(created_at_raw, str):
            # Only parse valid string values
            self.created_at = datetime.datetime.fromisoformat(created_at_raw)
        else:
            # Fallback to current UTC time if missing or invalid
            self.created_at = datetime.datetime.now(datetime.timezone.utc)

    def clear_history(self):
        """Clear chat history."""
        self.history = []
