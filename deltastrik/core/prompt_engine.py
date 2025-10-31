# deltastrik/core/prompt_engine.py
"""
Prompt engine for building Claude-like system instructions for DeltaStrik.
Handles persona templates, runtime context injection, and optional user overrides.
"""

import os
import yaml
from datetime import datetime
from typing import Dict, Any, Optional
from deltastrik.core.config import load_config


model: str = load_config().get("model")



DEFAULT_PERSONA = """
You are DeltaStrik, an advanced terminal-based AI assistant designed for developers.
Your responses should be:
- Clear, concise, and technically accurate
- Markdown-formatted when showing code or lists
- Calm and confident, never apologetic
Avoid unnecessary filler phrases. Always stay focused on the user’s question.
"""

def build_system_prompt(config: Optional[Dict[str, Any]] = None) -> str:
    """
    Build the system prompt using defaults + any YAML persona overrides.
    """
    config = config or {}

    # Step 1: locate the persona YAML (if provided)
    persona_path = config.get(
        "persona_file",
        os.path.expanduser("~/.deltastrik/system_prompt.yaml")
    )

    # Step 2: load YAML if it exists, else use default
    persona_text = DEFAULT_PERSONA
    if os.path.exists(persona_path):
        try:
            with open(persona_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                persona_text = data.get("prompt", DEFAULT_PERSONA)
        except Exception as e:
            persona_text = DEFAULT_PERSONA + f"\n(Note: Failed to load YAML: {e})"

    # Step 3: add runtime context (optional but nice)
    date_info = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    system_prompt = (
        f"{persona_text.strip()}\n\n"
        f"[Context: Running on model '{model}' at {date_info}]\n"
    )

    return system_prompt
