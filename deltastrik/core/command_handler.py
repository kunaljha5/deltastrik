"""
Command handler for DeltaStrik's terminal chat commands.
Supports built-in commands like /help, /init, etc.
"""

from typing import Optional
from deltastrik.utils.logging_utils import setup_logger

logger = setup_logger("command_handler")


class CommandHandler:
    """
    Central place to handle slash commands entered by the user.
    """
    def __init__(self, session_manager, client, system_prompt_builder=None, app=None):
        self.session = session_manager
        self.client = client
        self.build_system_prompt = system_prompt_builder
        self.app = app

    def handle(self, user_text: str) -> Optional[str]:
        """
        Parse and handle a slash command. Returns a system response string if matched,
        otherwise returns None (so the caller knows to treat it as a normal chat message).
        """
        if not user_text.startswith("/"):
            return None

        command = user_text.strip().split()[0].lower()
        args = user_text.strip().split()[1:]
        if command == "/help":
            return self._handle_help()
        elif command == "/init":
            return self._handle_init(args)
        elif command == "/clear":
            return self._handle_clear()
        elif command in ["/exit", "/quit", "exit", "quit"]:
            return self._handle_exit()
        else:
            return f"[Unknown command: {command}] Try /help for available commands."

    # -------------------------------------------------------
    # Command Implementations
    # -------------------------------------------------------
    @staticmethod
    def _handle_help() -> str:
        help_text = """[bold cyan]Available commands:[/bold cyan]

      /help   - Show this help message  
      /init   - Reset conversation and reload system prompt  
      /clear  - Clear chat history in this session
      /exit   - Exit the current session
    """
        return help_text
    def _handle_init(self, args) -> str:
        self.session.clear_history()
        new_prompt = self.build_system_prompt({})
        logger.debug(f"Session reinitialized with new system prompt. {new_prompt}")
        return "[green]Session reset.[/green] System prompt reloaded."


    def _handle_clear(self) -> str:
        self.session.clear_history()
        logger.debug("Chat history cleared.")
        return "[green]Chat cleared.[/green]"

    def _handle_exit(self) -> str:
        """Exit the TUI gracefully."""
        logger.info("User exited the application.")
        if self.app:
            # Tell the app to shut down cleanly
            self.app.exit()
        return "[yellow]Exiting DeltaStrik...[/yellow]"