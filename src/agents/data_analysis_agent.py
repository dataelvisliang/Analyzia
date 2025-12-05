"""Data analysis agent with CSV capabilities"""

import re
import streamlit as st
import matplotlib.pyplot as plt
from langchain_experimental.agents import create_pandas_dataframe_agent

from .base_agent import LLMAgent
from ..config import SYSTEM_TEMPLATE
from ..utils import VisualizationHandler
from ..tools import CustomStreamlitCallbackHandler, CustomPythonAstREPLTool


class DataAnalysisAgent(LLMAgent):
    """Class to handle LLM agent interactions for data analysis"""

    def __init__(self, df, response_processor, openrouter_api_key=None, model=None):
        super().__init__(openrouter_api_key, model)
        self.df = df
        self.response_processor = response_processor
        self.agent = None
        self.python_repl_tool = None

    def setup_agent(self, file_path):
        """Set up the CSV agent with OpenRouter LLM."""
        # Create system prompt with dataframe schema
        df_schema = "\n".join([f"- {col} ({self.df[col].dtype})" for col in self.df.columns])
        system_prompt = SYSTEM_TEMPLATE.format(df_schema=df_schema)

        # Make sure LLM is initialized
        if not self.llm and not self.initialize_llm():
            return None

        try:
            # Create custom Python REPL tool for figure capture
            self.python_repl_tool = CustomPythonAstREPLTool()
            # Set locals after initialization to avoid Pydantic issues
            self.python_repl_tool.locals = VisualizationHandler.get_execution_context(self.df)
            self.python_repl_tool.name = "python_repl_ast"
            self.python_repl_tool.description = (
                "A Python shell. Use this to execute python commands. "
                "Input should be a valid python command. "
                "When using this tool, you can access the pandas DataFrame 'df'."
            )

            # Create agent using pandas dataframe agent with ONLY our custom tool
            # The trick: pass empty extra_tools and modify the agent's tools list after creation
            self.agent = create_pandas_dataframe_agent(
                self.llm,
                self.df,
                verbose=True,
                agent_type="zero-shot-react-description",
                handle_parsing_errors=True,
                prefix=system_prompt,
                allow_dangerous_code=True,
                extra_tools=[],
                max_iterations=8,
                max_execution_time=60,
                early_stopping_method="generate"
            )

            # Replace the built-in PythonAstREPLTool with our custom one
            self.agent.tools = [self.python_repl_tool]

            return self.agent

        except Exception as e:
            st.error(f"Error setting up the agent: {str(e)}")
            return None

    def handle_chat_input(self, prompt):
        """Process chat input and handle agent responses."""
        try:
            # Create a container for the reasoning steps
            reasoning_container = st.container()

            with reasoning_container:
                # Show spinner while processing
                with st.spinner("🔍 Analyzing your question..."):
                    # Create status container for structured messages
                    status_container = st.empty()

                    # Custom callback handler with clean UI
                    custom_callback = CustomStreamlitCallbackHandler()

                    # Run the agent
                    raw_response = self.agent.run(prompt, callbacks=[custom_callback])

                    # Clear status messages
                    status_container.empty()

            # Process response for visualization
            processed_response = self.response_processor.process_response(raw_response)

            # Display the processed response
            st.write(processed_response)

            return raw_response

        except Exception as e:
            error_msg = str(e)

            # Try to extract the answer from parsing errors
            if "OUTPUT_PARSING_FAILURE" in error_msg or "Final Answer:" in error_msg:
                # Extract Final Answer from the error message
                import re
                match = re.search(r'Final Answer:\s*(.+?)(?:\n|$)', error_msg, re.DOTALL)
                if match:
                    answer = match.group(1).strip()
                    # Display the answer without showing the error
                    st.write(answer)
                    return answer

            # For other errors, show error message
            st.error(f"Error processing your question: {error_msg}")

            # Try to extract useful information from the error
            if "agent_scratchpad" in error_msg:
                st.warning("The AI had difficulty processing your request with the available data.")
                st.info("Try asking a simpler question or provide more context.")

            return f"I encountered an error processing your request: {error_msg}"

    def _extract_response_from_error(self, error_msg):
        """Extract meaningful response from parsing error messages."""
        # Strategy 1: Look for content between backticks
        backtick_pattern = r"`([^`]+)`"
        matches = re.findall(backtick_pattern, error_msg)
        if matches:
            # Get the longest match (likely the actual response)
            longest_match = max(matches, key=len)
            if len(longest_match) > 50:  # Reasonable response length
                return longest_match

        # Strategy 2: Look for "Could not parse LLM output:" and extract what follows
        parse_pattern = r"Could not parse LLM output:\s*(.+?)(?:\n\n|\Z)"
        match = re.search(parse_pattern, error_msg, re.DOTALL)
        if match:
            return match.group(1).strip()

        # Strategy 3: Look for actual analysis content in the error
        lines = error_msg.split('\n')
        content_lines = []
        capturing = False

        for line in lines:
            # Start capturing after common error prefixes
            if any(phrase in line for phrase in ["analysis", "data", "findings", "results"]):
                capturing = True

            if capturing and line.strip():
                # Skip obvious error message lines
                if not any(phrase in line.lower() for phrase in [
                    "error", "traceback", "exception", "could not parse", "parsing"
                ]):
                    content_lines.append(line)

        if content_lines:
            return '\n'.join(content_lines)

        return None

    def _direct_llm_fallback(self, prompt):
        """Direct LLM call as fallback when agent fails."""
        try:
            if not self.llm:
                return "I apologize, but I'm having technical difficulties processing your request."

            # Create a simplified prompt with data context
            df_info = f"Dataset shape: {self.df.shape}\nColumns: {', '.join(self.df.columns[:10])}"
            if len(self.df.columns) > 10:
                df_info += f"... and {len(self.df.columns) - 10} more columns"

            fallback_prompt = f"""
            As a data analyst, please analyze this request: "{prompt}"

            Dataset Information:
            {df_info}

            Please provide a comprehensive analysis with:
            1. Executive Summary
            2. Analysis approach
            3. Key insights based on the request
            4. Recommendations
            5. Next steps

            Note: I cannot execute code directly in this mode, so focus on analytical insights and methodology.
            """

            response = self.llm.invoke(fallback_prompt)

            # Add a note about the fallback mode
            fallback_response = f"""
## Analysis Report (Direct Mode)

*Note: This analysis was generated in direct mode due to technical constraints. For interactive visualizations and code execution, please try rephrasing your question.*

{response.content if hasattr(response, 'content') else str(response)}
            """

            return fallback_response

        except Exception as e:
            return f"""
## Analysis Error

I apologize, but I encountered technical difficulties processing your request.

**Error Details:** {str(e)}

**Suggestions:**
1. Try rephrasing your question in simpler terms
2. Break complex requests into smaller parts
3. Ensure your CSV data is properly formatted
4. Check if the column names in your question match the dataset

**Available Columns:** {', '.join(self.df.columns[:5])}{'...' if len(self.df.columns) > 5 else ''}
            """

    def display_question_input(self):
        """Display the question input field with minimal styling"""
        return st.chat_input("Ask me anything about your data...")
