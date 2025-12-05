"""OpenRouter LLM wrapper for LangChain"""

import requests
from langchain_core.language_models.llms import LLM
from pydantic import Field
from typing import Optional, List, Any


class OpenRouterLLM(LLM):
    """Custom LLM wrapper for OpenRouter API"""

    openrouter_api_key: str = Field(...)
    model: str = Field(default="x-ai/grok-4.1-fast:free")
    temperature: float = Field(default=0.7)
    max_tokens: Optional[int] = Field(default=None)

    @property
    def _llm_type(self) -> str:
        return "openrouter"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> str:
        """Call OpenRouter API"""
        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8502",
            "X-Title": "Analyzia Data Analysis"
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
        }

        if self.max_tokens:
            payload["max_tokens"] = self.max_tokens

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )

            # Get response text before raising for better error messages
            response_text = response.text

            if response.status_code != 200:
                error_detail = f"Status {response.status_code}: {response_text}"
                raise Exception(f"OpenRouter API error: {error_detail}")

            result = response.json()

            # Check if there's an error in the response
            if 'error' in result:
                raise Exception(f"OpenRouter API error: {result['error']}")

            return result['choices'][0]['message']['content']

        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenRouter API request failed: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Unexpected API response format: {str(e)}. Response: {response_text if 'response_text' in locals() else 'N/A'}")
