"""Small, low-token Gemini service.

The application keeps calculations deterministic in Python. Gemini is used for
short explanations, grounded market context and chat responses.
"""

from __future__ import annotations

import json
from typing import Any

from google import genai
from google.genai import types

from app.config import settings


class GeminiService:
    def __init__(self) -> None:
        self._client: genai.Client | None = None

    @property
    def client(self) -> genai.Client:
        if self._client is None:
            if not settings.gemini_api_key:
                raise RuntimeError(
                    "GEMINI_API_KEY is not configured. Add it to the project .env file."
                )
            self._client = genai.Client(api_key=settings.gemini_api_key)
        return self._client

    def generate(
        self,
        prompt: str,
        *,
        system_instruction: str | None = None,
        temperature: float = 0.2,
        max_output_tokens: int = 700,
    ) -> str:
        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            system_instruction=system_instruction,
        )
        response = self.client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=config,
        )
        return (response.text or "").strip()

    def research(
        self,
        prompt: str,
        *,
        system_instruction: str | None = None,
        max_output_tokens: int = 900,
    ) -> str:
        """One small grounded search call for current public market context."""
        config = types.GenerateContentConfig(
            temperature=0.1,
            max_output_tokens=max_output_tokens,
            system_instruction=system_instruction,
            tools=[types.Tool(google_search=types.GoogleSearch())],
        )
        response = self.client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=config,
        )
        return (response.text or "").strip()

    def generate_json(
        self,
        prompt: str,
        *,
        system_instruction: str | None = None,
        max_output_tokens: int = 700,
    ) -> dict[str, Any]:
        text = self.generate(
            prompt,
            system_instruction=system_instruction,
            temperature=0.1,
            max_output_tokens=max_output_tokens,
        )
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.replace("```json", "", 1).replace("```", "", 1).strip()
        value = json.loads(cleaned)
        if not isinstance(value, dict):
            raise RuntimeError("Gemini JSON response must be an object.")
        return value


gemini_service = GeminiService()
