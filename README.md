# DeltaStrik

A modern, terminal-based chat interface for Ollama, built with Python and Textual.

## Features

- **Clean TUI Interface**: Rich terminal UI powered by Textual
- **Session Management**: Maintains conversation history and context
- **Configurable**: Customize model parameters (temperature, max tokens, etc.)
- **System Prompts**: Support for custom system prompts
- **Real-time Status**: View response latency and connection status
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

[Add your license here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
