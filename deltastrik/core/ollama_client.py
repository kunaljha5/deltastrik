import requests
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin
from deltastrik.utils.logging_utils import setup_logger

logger = setup_logger("ollama_client")


class OllamaClient:
    def __init__(self, config: Dict[str, Any]):
        self.base_url = config.get("ollama_url", "http://127.0.0.1:11434")
        self.model = config.get("model", "gpt-oss:latest")
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 1024)
        self.stream = config.get("stream", False)
        self.timeout = config.get("timeout", 10)

    def query(self, prompt: str, user_message: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        messages = self._build_message_payload(prompt, user_message, history)

        payload = {
            "model": self.model,
            "messages": messages,
            "options": {"temperature": self.temperature, "num_predict": self.max_tokens},
            "stream": self.stream,
        }

        try:
            url_test = urljoin(self.base_url, "api/chat")
            logger.debug(f"Hitting Ollama at: {url_test}")
            logger.debug(f"Payload: {payload}")

            response = requests.post(url=url_test, json=payload, timeout=self.timeout)
            logger.info(f"Ollama response status: {response.status_code}")
            logger.debug(f"Ollama raw response: {response.text}")

            response.raise_for_status()
            data = response.json()
            return self._extract_reply(data)

        except Exception as e:
            logger.exception("Error contacting Ollama backend")
            return f"[Error contacting Ollama backend: {e}]"

    def _build_message_payload(self, prompt, user_message, history):
        messages = []
        if prompt:
            messages.append({"role": "system", "content": prompt})
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_message})
        return messages

    def _extract_reply(self, data: Dict[str, Any]) -> str:
        if "message" in data and "content" in data["message"]:
            content = data["message"]["content"]
            logger.debug(f"Extracted assistant reply: {content}")
            return content
        elif "error" in data:
            return f"[Ollama Error: {data['error']}]"
        else:
            logger.warning(f"Unexpected Ollama response: {data}")
            return "[No response received from Ollama]"

    def compress_generate(self, system_prompt: str, summary_prompt: str) -> str:
        """This generates a context short summary of the Ollama"""
        messages = self._build_message_payload(system_prompt, summary_prompt, history=None)

        payload = {
            "model": self.model,
            "messages": messages,
            "options": {"temperature": self.temperature, "num_predict": self.max_tokens},
            "stream": self.stream,
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "options": {"temperature": self.temperature, "num_predict": self.max_tokens},
            "stream": self.stream,
        }

        try:
            url_test = urljoin(self.base_url, "api/chat")
            logger.debug(f"Hitting Ollama at: {url_test}")
            logger.debug(f"Payload: {payload}")

            response = requests.post(url=url_test, json=payload, timeout=self.timeout)
            logger.info(f"Ollama response status: {response.status_code}")
            logger.debug(f"Ollama raw response: {response.text}")

            response.raise_for_status()
            data = response.json()
            return self._extract_reply(data)

        except Exception as e:
            logger.exception("Error contacting Ollama backend")
            return f"[Error contacting Ollama backend: {e}]"
