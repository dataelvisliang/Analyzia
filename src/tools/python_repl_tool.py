"""Custom Python REPL tool for code execution with figure capture"""

import streamlit as st
import matplotlib.pyplot as plt
from langchain_experimental.tools import PythonAstREPLTool


class CustomPythonAstREPLTool(PythonAstREPLTool):
    """Custom Python AST REPL Tool that captures and displays matplotlib/plotly figures in Streamlit"""

    def _run(self, query: str) -> str:
        """Run the query in the Python REPL and capture the result."""
        try:
            if self.locals is None:
                self.locals = {}

            print(f"[DEBUG] Executing query: {query[:100]}...")
            result = super()._run(query)
            print(f"[DEBUG] Execution result: {result}")

            # Display matplotlib figures immediately
            fig_nums = plt.get_fignums()
            print(f"[DEBUG] Matplotlib figures: {fig_nums}")
            if fig_nums:
                current_fig = plt.gcf()
                print(f"[DEBUG] Displaying matplotlib figure")
                st.pyplot(current_fig, use_container_width=True)
                plt.close(current_fig)
                result += "\n\nVisualization successfully displayed."

            # Display plotly figures immediately
            print(f"[DEBUG] Checking locals for plotly: {list(self.locals.keys())}")
            for var_name, var in self.locals.items():
                var_type = str(type(var))
                if 'plotly' in var_type.lower():
                    print(f"[DEBUG] Found plotly figure: {var_name}")
                    st.plotly_chart(var, use_container_width=True)
                    result += "\n\nVisualization successfully displayed."
                    break

            return result if result else ""

        except Exception as e:
            error_message = f"Error executing code: {str(e)}"
            print(f"[DEBUG] Error: {error_message}")
            st.error(error_message)
            return error_message
