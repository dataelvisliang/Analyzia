"""Response processor for handling agent outputs"""

import re
import streamlit as st
from ..utils import CodeUtils, VisualizationHandler


class ResponseProcessor:
    """Class to process and execute Python code from agent responses"""

    def __init__(self, df):
        self.df = df
        self.visualization_executed = False

    def process_response(self, response):
        """Process agent response to execute Python code visualizations and clean output."""

        if self.visualization_executed:
            self.visualization_executed = False
            return response

        # Extract Final Answer if present
        final_answer = self._extract_final_answer(response)
        if final_answer:
            response = final_answer

        # Extract and execute visualization code
        python_code = CodeUtils.extract_code_from_response(response)

        if python_code:
            try:
                success, message = VisualizationHandler.execute_visualization_code(python_code, self.df)

                if success:
                    self.visualization_executed = True

                cleaned_response = CodeUtils.remove_code_from_response(response, python_code)
                return cleaned_response
            except Exception as e:
                st.error(f"Error executing Python code: {str(e)}")

        return response

    def _extract_final_answer(self, response):
        """Extract the Final Answer section from agent response."""
        # Look for "Final Answer:" pattern
        patterns = [
            r"Final Answer:\s*(.+?)(?:\n\n|\Z)",
            r"Final Answer:\s*(.+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return None
