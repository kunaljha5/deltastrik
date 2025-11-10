# deltastrik/core/session_manager.py
"""
Manages chat sessions and message history for DeltaStrik.
Provides an interface for storing, retrieving, and serializing
conversation context between the user and the LLM (Ollama backend).
"""

from typing import List, Dict, Any
import datetime
from deltastrik.core.prompt_engine import build_system_prompt
from deltastrik.core.ollama_client import OllamaClient


class SessionManager:
    """
    Maintains conversation history and context.
    """

    def __init__(self, config):
        # Chat history follows the typical OpenAI/Ollama format:
        # [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
        self.config = config
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

    def compact(self, instructions: str | None = None) -> str:
        """
        Summarize and compact the chat history into a single system summary.
        """
        if not self.history:
            return "⚠️ No history to compact."

        # Step 1: Build summarization prompt
        summary_prompt = "Summarize the following conversation in a way that retains all essential context, goals, and facts for future continuation.\n"
        if instructions:
            summary_prompt += f"\nAdditional instructions: {instructions}\n"

        summary_prompt += "\n--- Conversation ---\n"
        for msg in self.history:
            summary_prompt += f"{msg['role']}: {msg['content']}\n"

        # Step 2: Call local model to summarize
        ollama = OllamaClient(config=self.config)
        system_prompt = build_system_prompt()
        summary_response = ollama.compress_generate(system_prompt, summary_prompt)

        summary_text = summary_response.strip()

        # Step 3: Replace full history with summary as system message
        self.history = [{"role": "system", "content": summary_text}]
        # self.save_session()

        return "✅ Conversation compacted. Summary retained in system context."
