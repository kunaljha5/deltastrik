# DeltaStrik

An experimental terminal chat client for Ollama, developed in Python using the Textual framework.

## Features

- **Clean TUI Interface**: Rich terminal UI powered by Textual
- **Session Management**: Maintains conversation history and context
- **Configurable**: Customize model parameters (temperature, max tokens, etc.)
- **System Prompts**: Support for custom system prompts
- **Real-time Status**: View response latency and connection status
- **Processing Indicators**: Visual feedback while waiting for AI responses
- **Command Autocomplete**: Tab completion for slash commands
- **Command History**: Navigate previous commands with up/down arrows
- **Easy Text Copying**: Hold Shift to select and copy text from the TUI
- **Session Export**: Save and load conversation sessions
- **Logging**: Built-in debug logging for troubleshooting

## Requirements

- Python 3.12+
- Ollama running locally (default: http://127.0.0.1:11434)

## Installation

```bash
pip install deltastrik
```

## Usage

```bash
deltastrik
```

### Keyboard Shortcuts

- **Enter**: Send message
- **Up/Down Arrows**: Navigate command history
- **Escape**: Toggle between input and chat view (for scrolling)
- **Ctrl+M**: Show instructions for copying text
- **Shift+Mouse**: Select and copy text from the chat

### Available Commands

Type `/` to see autocomplete suggestions:

- `/help` - Show available commands
- `/init` - Reset conversation and reload system prompt
- `/clear` - Clear chat history
- `/copy` - Show instructions for copying text
- `/exit` or `/quit` - Exit the application

## Configuration

DeltaStrik supports configuration for:
- Model selection (default: gpt-oss:latest)
- Temperature (default: 0.7)
- Max tokens (default: 1024)
- Ollama URL (default: http://127.0.0.1:11434)

## Development

```bash
# Install dependencies
pip install -e .

# Run tests
pytest

# Build
python -m build
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
