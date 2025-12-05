# Analyzia Developer Guide

## Quick Start

### Running the Application
```bash
streamlit run app.py
```

### Running Tests
```bash
# Test imports
python -c "from src.agents import DataAnalysisAgent; from src.utils import CodeUtils; print('✓ All modules loaded')"
```

## Module Reference

### 1. Agents (`src/agents/`)

#### `OpenRouterLLM`
Custom LangChain LLM wrapper for OpenRouter API.

```python
from src.agents import OpenRouterLLM

llm = OpenRouterLLM(
    openrouter_api_key="your-key",
    model="nousresearch/hermes-3-llama-3.1-405b:free",
    temperature=0.7,
    max_tokens=4000
)
```

#### `DataAnalysisAgent`
Main agent for CSV data analysis.

```python
from src.agents import DataAnalysisAgent, ResponseProcessor

processor = ResponseProcessor(df)
agent = DataAnalysisAgent(df, processor, api_key, model)
agent.setup_agent(file_path)
response = agent.handle_chat_input("Show rating over time")
```

#### `ResponseProcessor`
Processes agent responses to extract and execute code.

```python
from src.agents import ResponseProcessor

processor = ResponseProcessor(df)
cleaned_response = processor.process_response(raw_response)
```

### 2. Tools (`src/tools/`)

#### `CustomStreamlitCallbackHandler`
Callback handler for Streamlit UI updates.

```python
from src.tools import CustomStreamlitCallbackHandler

callback = CustomStreamlitCallbackHandler()
response = agent.run(prompt, callbacks=[callback])
```

#### `CustomPythonAstREPLTool`
Python REPL that captures matplotlib figures.

```python
from src.tools import CustomPythonAstREPLTool

tool = CustomPythonAstREPLTool(locals={'df': df, 'plt': plt})
result = tool._run("plt.plot([1,2,3])")
CustomPythonAstREPLTool.display_pending_figures()  # Show captured figures
```

### 3. Utils (`src/utils/`)

#### `CodeUtils`
Extract and sanitize Python code from responses.

```python
from src.utils import CodeUtils

# Extract code from response
code = CodeUtils.extract_code_from_response(response)

# Sanitize code (remove plt.show())
clean_code = CodeUtils.sanitize_code(code)

# Remove code from response text
text = CodeUtils.remove_code_from_response(response, code)
```

#### `VisualizationHandler`
Execute visualization code safely.

```python
from src.utils import VisualizationHandler

# Get execution context
context = VisualizationHandler.get_execution_context(df)

# Execute visualization
success, msg = VisualizationHandler.execute_visualization_code(
    code, df, display=True
)
```

#### `DataFrameUtils`
Display DataFrame information in Streamlit.

```python
from src.utils import DataFrameUtils

DataFrameUtils.display_dataframe_info(df)
```

### 4. Config (`src/config/`)

#### Models
```python
from src.config import AVAILABLE_MODELS, DEFAULT_MODEL

print(DEFAULT_MODEL)  # nousresearch/hermes-3-llama-3.1-405b:free
print(AVAILABLE_MODELS)  # List of all available models
```

#### Prompts
```python
from src.config import SYSTEM_TEMPLATE, COMMON_SYSTEM_TEMPLATE

# Use in agent setup
df_schema = "..."
prompt = SYSTEM_TEMPLATE.format(df_schema=df_schema)
```

## Common Tasks

### Adding a New Model

Edit [src/config/models.py](src/config/models.py):

```python
AVAILABLE_MODELS = [
    "nousresearch/hermes-3-llama-3.1-405b:free",
    # Add your new model here
    "provider/new-model-name:free",
]
```

### Modifying System Prompts

Edit [src/config/prompts.py](src/config/prompts.py):

```python
SYSTEM_TEMPLATE = """
Your updated prompt here...
{df_schema}
"""
```

### Adding a New Utility Function

Create a new function in the appropriate utils module:

```python
# src/utils/code_utils.py

@staticmethod
def your_new_function(code):
    """Your function description"""
    # Implementation
    return result
```

### Creating a New Agent Type

1. Create new file: `src/agents/your_agent.py`
2. Inherit from `LLMAgent`:

```python
from .base_agent import LLMAgent

class YourAgent(LLMAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Your initialization

    def your_method(self):
        # Your implementation
        pass
```

3. Add to `src/agents/__init__.py`:

```python
from .your_agent import YourAgent

__all__ = [..., 'YourAgent']
```

### Adding a Custom Tool

1. Create new file: `src/tools/your_tool.py`
2. Inherit from appropriate LangChain base class:

```python
from langchain.tools import BaseTool

class YourTool(BaseTool):
    name = "your_tool"
    description = "What your tool does"

    def _run(self, query: str) -> str:
        # Implementation
        return result
```

3. Add to `src/tools/__init__.py`

## Code Style Guidelines

### 1. Imports
```python
# Standard library
import os
import re

# Third-party
import streamlit as st
import pandas as pd

# Local
from src.agents import DataAnalysisAgent
from src.utils import CodeUtils
```

### 2. Docstrings
```python
def function_name(param1, param2):
    """Brief description of function.

    Args:
        param1: Description
        param2: Description

    Returns:
        Description of return value
    """
    pass
```

### 3. Type Hints (Optional but Recommended)
```python
from typing import Optional, List

def process_data(df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
    """Process DataFrame with optional column filtering."""
    pass
```

## Debugging Tips

### Enable Verbose Mode
The agent is already configured with `verbose=True`, which prints reasoning steps.

### Check Imports
```python
import sys
print(sys.path)  # Verify src is in path
```

### Test Individual Modules
```python
# Test utils
from src.utils import CodeUtils
code = CodeUtils.extract_code_from_response("```python\nprint('hi')\n```")
print(code)  # Should print: print('hi')

# Test config
from src.config import AVAILABLE_MODELS
print(len(AVAILABLE_MODELS))  # Should print: 8
```

### Debug Agent Responses
```python
# In data_analysis_agent.py, add logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Add debug prints
print(f"DEBUG: Response from agent: {raw_response}")
```

## Performance Optimization

### 1. Reduce Token Usage
Edit `src/config/prompts.py` to use shorter prompts.

### 2. Cache Results
```python
import streamlit as st

@st.cache_data
def expensive_operation(df):
    # Cached operation
    return result
```

### 3. Optimize Model Selection
Use smaller models for simple queries in `src/config/models.py`.

## Troubleshooting

### Import Errors
```bash
# Ensure you're in the right directory
cd "path/to/Analyzia"

# Verify structure
ls src/agents/
```

### Module Not Found
```python
# Add to PYTHONPATH if needed
import sys
sys.path.insert(0, '/path/to/Analyzia')
```

### Matplotlib Figures Not Displaying
Check `CustomPythonAstREPLTool` class variables:
```python
print(CustomPythonAstREPLTool._pending_figures)  # Should show captured figures
```

## Contributing

1. Follow the existing structure
2. Add docstrings to all functions
3. Test imports after changes
4. Update `__init__.py` files when adding new modules
5. Document new features in this guide

## Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenRouter API](https://openrouter.ai/docs)
- [Analyzia GitHub](https://github.com/ahammadnafiz/Analyzia)
