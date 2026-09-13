import os

import requests
from dotenv import load_dotenv


load_dotenv()


class LLMClient:

    def __init__(
        self,
        base_url=None,
        model=None,
        timeout=120,
    ):
        self.base_url = (
            base_url
            or os.getenv(
                "OLLAMA_URL",
                "http://localhost:11434",
            )
        )

        self.model = (
            model
            or os.getenv(
                "OLLAMA_MODEL",
                "qwen3",
            )
        )

        self.timeout = timeout

    def generate_text(self, prompt):
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                "stream": False,
            },
            timeout=self.timeout,
        )

        response.raise_for_status()

        data = response.json()

        return data["message"]["content"]