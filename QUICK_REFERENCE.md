# Analyzia Quick Reference

## Project Structure (One-Liner)
```
src/{agents,tools,utils,config}/ - Modular code | app.py - Main entry point
```

## Running the App
```bash
streamlit run app.py
```

## Directory Layout
```
src/
├── agents/     # LLM & analysis logic
├── tools/      # Custom LangChain tools
├── utils/      # Helper functions
└── config/     # Settings & prompts
```

## Quick Module Import Guide

### Agents
```python
from src.agents import DataAnalysisAgent, ResponseProcessor, OpenRouterLLM
```

### Tools
```python
from src.tools import CustomStreamlitCallbackHandler, CustomPythonAstREPLTool
```

### Utils
```python
from src.utils import CodeUtils, VisualizationHandler, DataFrameUtils
```

### Config
```python
from src.config import AVAILABLE_MODELS, DEFAULT_MODEL, SYSTEM_TEMPLATE
```

## Common Tasks

### Add a New Model
**File**: `src/config/models.py`
```python
AVAILABLE_MODELS = [
    "existing-model",
    "your-new-model:free",  # Add here
]
```

### Modify System Prompt
**File**: `src/config/prompts.py`
```python
SYSTEM_TEMPLATE = """
Your updated prompt...
{df_schema}
"""
```

### Add Utility Function
**File**: `src/utils/code_utils.py` (or appropriate utils file)
```python
@staticmethod
def your_function(input):
    """Description"""
    return output
```

### Debug Agent Response
**File**: `src/agents/data_analysis_agent.py`
```python
# In handle_chat_input(), add:
print(f"DEBUG: {raw_response}")
```

## Module Responsibilities

| Module | What It Does |
|--------|--------------|
| `agents/openrouter_llm.py` | OpenRouter API communication |
| `agents/base_agent.py` | LLM initialization |
| `agents/data_analysis_agent.py` | Main CSV agent logic |
| `agents/response_processor.py` | Clean & extract from responses |
| `tools/callback_handler.py` | UI feedback during execution |
| `tools/python_repl_tool.py` | Code execution + figure capture |
| `utils/code_utils.py` | Extract/sanitize code |
| `utils/visualization_handler.py` | Execute viz code |
| `utils/dataframe_utils.py` | Display DataFrame info |
| `config/models.py` | Available models list |
| `config/prompts.py` | System prompts |

## File Sizes

| File | Lines | Purpose |
|------|-------|---------|
| `app.py` | 330 | Main application |
| `src/agents/data_analysis_agent.py` | 220 | Main agent |
| `src/config/prompts.py` | 180 | Prompts |
| `src/agents/openrouter_llm.py` | 75 | API wrapper |
| Others | <70 | Support modules |

## Import Tree
```
app.py
├── src.agents.DataAnalysisAgent
│   ├── src.agents.LLMAgent
│   │   └── src.agents.OpenRouterLLM
│   ├── src.tools.CustomPythonAstREPLTool
│   ├── src.tools.CustomStreamlitCallbackHandler
│   └── src.utils.VisualizationHandler
├── src.agents.ResponseProcessor
│   ├── src.utils.CodeUtils
│   └── src.utils.VisualizationHandler
├── src.utils.DataFrameUtils
└── src.config.AVAILABLE_MODELS
```

## Key Classes & Their Methods

### DataAnalysisAgent
```python
agent = DataAnalysisAgent(df, processor, api_key, model)
agent.setup_agent(file_path)           # Initialize CSV agent
response = agent.handle_chat_input(prompt)  # Process user query
```

### ResponseProcessor
```python
processor = ResponseProcessor(df)
clean = processor.process_response(raw)  # Extract & execute code
```

### CustomPythonAstREPLTool
```python
tool = CustomPythonAstREPLTool(locals={...})
result = tool._run(code)                 # Execute code
tool.display_pending_figures()           # Show captured plots
```

### CodeUtils
```python
code = CodeUtils.extract_code_from_response(response)
clean = CodeUtils.sanitize_code(code)
text = CodeUtils.remove_code_from_response(response, code)
```

### VisualizationHandler
```python
ctx = VisualizationHandler.get_execution_context(df)
ok, msg = VisualizationHandler.execute_visualization_code(code, df)
```

## Configuration Files

### models.py
```python
AVAILABLE_MODELS = [...]  # List of model IDs
DEFAULT_MODEL = "..."     # Default selection
```

### prompts.py
```python
SYSTEM_TEMPLATE = "..."        # Main agent prompt
COMMON_SYSTEM_TEMPLATE = "..."  # Extended template
```

## Testing Quick Commands

```bash
# Test imports
python -c "from src.agents import DataAnalysisAgent; print('✓')"

# Test all modules
python -c "from src.agents import *; from src.utils import *; from src.config import *; print('✓')"

# Run app
streamlit run app.py
```

## Debugging Tips

### Enable Verbose Logging
Agent already has `verbose=True` in `data_analysis_agent.py:798`

### Check Figure Capture
```python
print(CustomPythonAstREPLTool._pending_figures)
```

### Inspect Response
```python
# In handle_chat_input()
print(f"Raw: {raw_response}")
print(f"Processed: {processed_response}")
```

## Common Error Solutions

### ImportError: No module named 'src'
```bash
# Ensure you're in the Analyzia directory
cd path/to/Analyzia
python app.py  # or streamlit run app.py
```

### Figures Not Displaying
Check `CustomPythonAstREPLTool._pending_figures` has figures

### API Errors
Verify API key in sidebar and check model availability

## Performance Tips

1. **Use smaller models** for simple queries (edit `DEFAULT_MODEL`)
2. **Cache results** with `@st.cache_data` in app.py
3. **Reduce prompt size** in `prompts.py` if needed

## Code Style

### Imports Order
```python
# 1. Standard library
import os
import re

# 2. Third-party
import streamlit as st
import pandas as pd

# 3. Local
from src.agents import DataAnalysisAgent
```

### Docstrings
```python
def function(param):
    """Brief description.

    Args:
        param: Description

    Returns:
        Description
    """
```

## Git Workflow

```bash
# See changes
git status

# View structure
find src -name "*.py"

# Backup before changes
cp app.py app_backup_$(date +%Y%m%d).py
```

## Documentation Files

- `STRUCTURE.md` - Project layout
- `REFACTORING_SUMMARY.md` - What changed
- `DEVELOPER_GUIDE.md` - Full dev guide
- `ARCHITECTURE.md` - System design
- `CHANGES.md` - Detailed changelog
- `QUICK_REFERENCE.md` - This file

## Version Info

- **Original**: 1315 lines, single file
- **Refactored**: 16 files, ~1100 total lines
- **Main app**: 330 lines (75% reduction)
- **Status**: ✅ Tested and working

## Contact & Links

- GitHub: https://github.com/ahammadnafiz/Analyzia
- OpenRouter: https://openrouter.ai/
- Streamlit Docs: https://docs.streamlit.io/
- LangChain Docs: https://python.langchain.com/

---

**Last Updated**: 2025-12-04
**Version**: 1.0.0 (Modular)
