"""Custom callback handler for Streamlit UI"""

import streamlit as st
from langchain_core.callbacks import BaseCallbackHandler
from typing import Dict, Any


class CustomStreamlitCallbackHandler(BaseCallbackHandler):
    """Custom callback handler for better Streamlit UI without thinking face emoji"""

    def __init__(self):
        self.step_container = None
        self.current_step = 0

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs) -> None:
        """Called when chain starts"""
        pass

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs) -> None:
        """Called when chain ends"""
        pass

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs) -> None:
        """Called when tool starts - show what the agent is doing"""
        tool_name = serialized.get("name", "tool")
        self.current_step += 1

        # Don't show python_repl_ast execution in status boxes to avoid blocking chart display
        if tool_name == "python_repl_ast":
            # Just log that code is running, don't create a status container
            pass
        else:
            with st.status(f"Step {self.current_step}: Using {tool_name}", expanded=False):
                st.write(input_str)

    def on_tool_end(self, output: str, **kwargs) -> None:
        """Called when tool ends"""
        pass

    def on_llm_start(self, serialized: Dict[str, Any], prompts: list[str], **kwargs) -> None:
        """Called when LLM starts"""
        pass

    def on_llm_end(self, response, **kwargs) -> None:
        """Called when LLM ends"""
        pass
