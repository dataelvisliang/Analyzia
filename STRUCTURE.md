# Analyzia - Project Structure

This document describes the modular structure of the Analyzia application.

## Directory Structure

```
Analyzia/
├── app.py                          # Main application entry point (streamlined)
├── app_backup.py                   # Backup of original monolithic app
├── src/                            # Source code modules
│   ├── __init__.py
│   ├── agents/                     # AI agents and LLM integration
│   │   ├── __init__.py
│   │   ├── base_agent.py          # Base agent class with common functionality
│   │   ├── data_analysis_agent.py # Main data analysis agent
│   │   ├── openrouter_llm.py      # OpenRouter API wrapper
│   │   └── response_processor.py  # Process and clean agent responses
│   ├── tools/                      # Custom tools and callbacks
│   │   ├── __init__.py
│   │   ├── callback_handler.py    # Streamlit UI callback handler
│   │   └── python_repl_tool.py    # Custom Python REPL with figure capture
│   ├── utils/                      # Utility functions
│   │   ├── __init__.py
│   │   ├── code_utils.py          # Code extraction and sanitization
│   │   ├── dataframe_utils.py     # DataFrame display utilities
│   │   └── visualization_handler.py # Visualization execution
│   └── config/                     # Configuration and constants
│       ├── __init__.py
│       ├── models.py              # Available AI models
│       └── prompts.py             # System prompts and templates
└── requirements.txt                # Python dependencies
```

## Module Descriptions

### `app.py`
The main application entry point. Contains the `DataApp` class that orchestrates:
- Page configuration
- UI rendering (sidebar, header, status messages)
- File upload and processing
- Chat interaction handling

### `src/agents/`
Contains all LLM-related functionality:

- **`base_agent.py`**: Base class for all agents with LLM initialization
- **`data_analysis_agent.py`**: Main CSV analysis agent with:
  - Agent setup and configuration
  - Chat input handling
  - Error recovery strategies
  - Fallback mechanisms
- **`openrouter_llm.py`**: Custom LangChain LLM wrapper for OpenRouter API
- **`response_processor.py`**: Processes agent responses to extract and execute code

### `src/tools/`
Custom LangChain tools and callback handlers:

- **`callback_handler.py`**: Custom Streamlit callback for better UI feedback
- **`python_repl_tool.py`**: Enhanced Python REPL that captures matplotlib figures

### `src/utils/`
Utility functions for common operations:

- **`code_utils.py`**: Extract and sanitize Python code from responses
- **`dataframe_utils.py`**: Display DataFrame information in Streamlit
- **`visualization_handler.py`**: Execute visualization code with proper context

### `src/config/`
Application configuration:

- **`models.py`**: List of available OpenRouter models and default selection
- **`prompts.py`**: System prompts and templates for the AI agent

## Benefits of This Structure

1. **Modularity**: Each component has a single responsibility
2. **Maintainability**: Easy to locate and update specific functionality
3. **Testability**: Individual modules can be tested in isolation
4. **Reusability**: Components can be reused in other projects
5. **Scalability**: Easy to add new features or agents
6. **Readability**: Clear separation of concerns

## Usage

Run the application with:
```bash
streamlit run app.py
```

## Migration from Old Structure

The original monolithic `app.py` (1315 lines) has been refactored into:
- Main app: ~330 lines
- 9 separate modules with focused responsibilities
- Total reduction in complexity while maintaining all functionality

The backup of the original file is saved as `app_backup.py`.
