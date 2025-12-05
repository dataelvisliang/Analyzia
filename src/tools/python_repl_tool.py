"""Custom Python REPL tool for code execution with figure capture"""

import re
import streamlit as st
import matplotlib.pyplot as plt
from langchain_experimental.tools import PythonAstREPLTool
from typing import Any, Dict, Optional


class CustomPythonAstREPLTool(PythonAstREPLTool):
    """Custom Python AST REPL Tool that captures matplotlib figures for later display"""

    # Use class variable to store pending figures (not instance variable to avoid Pydantic validation)
    _pending_figures = []

    class Config:
        """Pydantic config to allow arbitrary types"""
        arbitrary_types_allowed = True

    def _run(self, query: str) -> str:
        """Run the query in the Python REPL and capture figures without displaying."""
        try:
            if self.locals is None:
                self.locals = {}

            # Remove plt.show() if present
            query_cleaned = re.sub(r'plt\.show\(\)\s*', '', query)

            # Execute the code
            result = super()._run(query_cleaned)

            # Check for figures in the exec namespace (not global matplotlib)
            plt_from_locals = self.locals.get('plt', plt)
            if hasattr(plt_from_locals, 'get_fignums') and plt_from_locals.get_fignums():
                # Capture all figures from the execution context
                CustomPythonAstREPLTool._pending_figures = [
                    plt_from_locals.figure(num) for num in plt_from_locals.get_fignums()
                ]
                result = "[Visualization created]"

            return result if result else ""

        except Exception as e:
            error_message = f"Error executing code: {str(e)}"
            return error_message

    @classmethod
    def display_pending_figures(cls):
        """Display all pending figures that were captured during execution."""
        for fig in cls._pending_figures:
            try:
                st.pyplot(fig, use_container_width=True)
            except:
                st.pyplot(fig)
            finally:
                plt.close(fig)
        cls._pending_figures = []
