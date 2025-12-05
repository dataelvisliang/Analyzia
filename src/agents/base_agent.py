"""Base agent class with common functionality"""

import streamlit as st
from .openrouter_llm import OpenRouterLLM
from ..config import DEFAULT_MODEL


class LLMAgent:
    """Base class for LLM agents with common functionality"""

    def __init__(self, openrouter_api_key=None, model=None):
        self.openrouter_api_key = openrouter_api_key
        self.model = model or DEFAULT_MODEL
        self.llm = None

    def initialize_llm(self):
        """Initialize the LLM with OpenRouter API"""
        if not self.openrouter_api_key:
            return False

        try:
            # Use custom OpenRouter LLM wrapper
            self.llm = OpenRouterLLM(
                openrouter_api_key=self.openrouter_api_key,
                model=self.model,
                temperature=0.7,
                max_tokens=4000
            )
            return True
        except Exception as e:
            st.error(f"Error initializing OpenRouter LLM: {str(e)}")
            return False
