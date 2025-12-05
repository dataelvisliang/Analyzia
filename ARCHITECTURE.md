# Analyzia Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                          User Interface                          │
│                        (Streamlit App)                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Main Application                           │
│                          (app.py)                                │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ • Page Configuration                                        │ │
│  │ • Sidebar Rendering (API key, model selection, file upload)│ │
│  │ • Chat Interface Management                                 │ │
│  │ • Session State Management                                  │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│   Agents       │  │    Tools       │  │    Utils       │
│   Module       │  │    Module      │  │    Module      │
└────────────────┘  └────────────────┘  └────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
    [Details below]      [Details below]     [Details below]
```

## Module Architecture

### 1. Agents Module (`src/agents/`)

```
┌──────────────────────────────────────────────────────────┐
│                    Agents Module                          │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  ┌────────────────────────────────────────────────────┐  │
│  │              OpenRouterLLM                          │  │
│  │  • API communication                                │  │
│  │  • Request/response handling                        │  │
│  │  • Error management                                 │  │
│  └────────────────────────────────────────────────────┘  │
│                        │                                  │
│                        ▼                                  │
│  ┌────────────────────────────────────────────────────┐  │
│  │              LLMAgent (Base)                        │  │
│  │  • LLM initialization                               │  │
│  │  • Common functionality                             │  │
│  └────────────────────────────────────────────────────┘  │
│                        │                                  │
│                        ▼                                  │
│  ┌────────────────────────────────────────────────────┐  │
│  │          DataAnalysisAgent                          │  │
│  │  • CSV agent setup                                  │  │
│  │  • Chat handling                                    │  │
│  │  • Error recovery                                   │  │
│  │  • Fallback strategies                              │  │
│  └────────────────────────────────────────────────────┘  │
│                        │                                  │
│                        ▼                                  │
│  ┌────────────────────────────────────────────────────┐  │
│  │          ResponseProcessor                          │  │
│  │  • Code extraction                                  │  │
│  │  • Response cleaning                                │  │
│  │  • Final answer extraction                          │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

### 2. Tools Module (`src/tools/`)

```
┌──────────────────────────────────────────────────────────┐
│                    Tools Module                           │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  ┌────────────────────────────────────────────────────┐  │
│  │      CustomStreamlitCallbackHandler                 │  │
│  │  • UI feedback during agent execution               │  │
│  │  • Step tracking                                    │  │
│  │  • Status updates                                   │  │
│  └────────────────────────────────────────────────────┘  │
│                                                           │
│  ┌────────────────────────────────────────────────────┐  │
│  │      CustomPythonAstREPLTool                        │  │
│  │  • Safe Python code execution                       │  │
│  │  • Matplotlib figure capture                        │  │
│  │  • plt.show() removal                               │  │
│  │  • Deferred figure display                          │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

### 3. Utils Module (`src/utils/`)

```
┌──────────────────────────────────────────────────────────┐
│                    Utils Module                           │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  ┌────────────────────────────────────────────────────┐  │
│  │              CodeUtils                              │  │
│  │  • extract_code_from_response()                     │  │
│  │  • sanitize_code()                                  │  │
│  │  • remove_code_from_response()                      │  │
│  └────────────────────────────────────────────────────┘  │
│                                                           │
│  ┌────────────────────────────────────────────────────┐  │
│  │          VisualizationHandler                       │  │
│  │  • get_execution_context()                          │  │
│  │  • execute_visualization_code()                     │  │
│  │  • Figure management                                │  │
│  └────────────────────────────────────────────────────┘  │
│                                                           │
│  ┌────────────────────────────────────────────────────┐  │
│  │           DataFrameUtils                            │  │
│  │  • display_dataframe_info()                         │  │
│  │  • DataFrame formatting                             │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

### 4. Config Module (`src/config/`)

```
┌──────────────────────────────────────────────────────────┐
│                   Config Module                           │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  ┌────────────────────────────────────────────────────┐  │
│  │              models.py                              │  │
│  │  • AVAILABLE_MODELS                                 │  │
│  │  • DEFAULT_MODEL                                    │  │
│  └────────────────────────────────────────────────────┘  │
│                                                           │
│  ┌────────────────────────────────────────────────────┐  │
│  │              prompts.py                             │  │
│  │  • SYSTEM_TEMPLATE                                  │  │
│  │  • COMMON_SYSTEM_TEMPLATE                           │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

## Data Flow

### Chat Input Processing Flow

```
User Input
    │
    ▼
Chat Input Handler (app.py)
    │
    ├─── No File? ──> Display "Upload File" Message
    │
    ├─── No API Key? ──> Display "Enter API Key" Message
    │
    └─── All Good ──> DataAnalysisAgent.handle_chat_input()
                           │
                           ▼
                    Create Callback Handler
                           │
                           ▼
                    Run Agent with Callbacks
                           │
                           ├─── Success ──> Get Response
                           │
                           ├─── Parsing Error ──> Extract from Error
                           │
                           └─── Total Failure ──> Fallback to Direct LLM
                           │
                           ▼
                    Display Pending Figures
                           │
                           ▼
                    ResponseProcessor.process_response()
                           │
                           ├─── Extract Final Answer
                           │
                           ├─── Extract Code
                           │
                           └─── Clean Response
                           │
                           ▼
                    Display to User
```

### Code Execution Flow

```
Agent generates code
    │
    ▼
CustomPythonAstREPLTool._run()
    │
    ├─── Remove plt.show()
    │
    ├─── Execute code
    │
    ├─── Capture figures
    │        │
    │        └─── Store in _pending_figures
    │
    └─── Return result
    │
    ▼
Agent completes
    │
    ▼
CustomPythonAstREPLTool.display_pending_figures()
    │
    └─── Display all captured figures
         │
         └─── Close figures
```

### Visualization Execution Flow

```
Code extracted from response
    │
    ▼
CodeUtils.sanitize_code()
    │
    └─── Remove plt.show()
    │
    ▼
VisualizationHandler.get_execution_context()
    │
    └─── Create context with df, plt, np, pd, sns
    │
    ▼
VisualizationHandler.execute_visualization_code()
    │
    ├─── Create figure and axes
    │
    ├─── Execute code in context
    │
    ├─── Apply tight_layout
    │
    ├─── Rotate labels if needed
    │
    └─── Display in Streamlit
         │
         └─── Close figure
```

## Component Interaction Diagram

```
┌────────────┐         ┌─────────────┐         ┌────────────┐
│            │         │             │         │            │
│   User     │────────▶│  Streamlit  │────────▶│  DataApp   │
│            │         │     UI      │         │            │
└────────────┘         └─────────────┘         └────────────┘
                                                      │
                                                      │
                       ┌──────────────────────────────┼──────────────────────────────┐
                       │                              │                              │
                       ▼                              ▼                              ▼
              ┌─────────────────┐         ┌──────────────────┐          ┌──────────────────┐
              │ DataAnalysis    │         │   Response       │          │  Visualization   │
              │    Agent        │────────▶│   Processor      │◀─────────│    Handler       │
              └─────────────────┘         └──────────────────┘          └──────────────────┘
                       │                              │
                       │                              │
                       ▼                              ▼
              ┌─────────────────┐         ┌──────────────────┐
              │  OpenRouter     │         │   Code Utils     │
              │      LLM        │         │                  │
              └─────────────────┘         └──────────────────┘
                       │
                       │
                       ▼
              ┌─────────────────┐
              │ Custom Python   │
              │   REPL Tool     │
              └─────────────────┘
```

## Key Design Patterns

### 1. Separation of Concerns
- **UI Layer**: Streamlit app (app.py)
- **Business Logic**: Agents and tools
- **Utilities**: Reusable functions
- **Configuration**: Centralized settings

### 2. Dependency Injection
```python
# ResponseProcessor injected into DataAnalysisAgent
processor = ResponseProcessor(df)
agent = DataAnalysisAgent(df, processor, api_key, model)
```

### 3. Factory Pattern
```python
# LLM creation in base agent
def initialize_llm(self):
    self.llm = OpenRouterLLM(...)
    return self.llm
```

### 4. Strategy Pattern
```python
# Multiple extraction strategies in DataAnalysisAgent
def _extract_response_from_error(self, error_msg):
    # Strategy 1: Backtick pattern
    # Strategy 2: Parse pattern
    # Strategy 3: Content analysis
```

### 5. Template Method Pattern
```python
# Base agent defines template, subclasses implement details
class LLMAgent:
    def initialize_llm(self):  # Template method
        ...

class DataAnalysisAgent(LLMAgent):
    def setup_agent(self):  # Specific implementation
        ...
```

## Error Handling Strategy

```
Error Occurs
    │
    ├─── Parsing Error?
    │        │
    │        ├─── Try extraction strategies
    │        │
    │        ├─── Retry without callbacks
    │        │
    │        └─── Direct LLM fallback
    │
    ├─── API Error?
    │        │
    │        └─── Show error + suggestions
    │
    └─── Execution Error?
             │
             └─── Display error + code
```

## Security Considerations

1. **Dangerous Code Execution**: Sandboxed in `CustomPythonAstREPLTool`
2. **API Key Management**: Stored in session, not persisted
3. **File Upload**: Temporary files, cleaned up automatically
4. **Code Sanitization**: `plt.show()` removal prevents hanging

## Performance Optimizations

1. **Lazy Loading**: Modules imported only when needed
2. **Figure Capture**: Deferred display prevents blocking
3. **Callback Optimization**: Skips UI updates for code execution
4. **Error Recovery**: Multiple fallback strategies prevent failures

## Extensibility Points

1. **New Models**: Add to `src/config/models.py`
2. **New Agents**: Inherit from `LLMAgent`
3. **New Tools**: Add to `src/tools/`
4. **New Utils**: Add to `src/utils/`
5. **Custom Prompts**: Modify `src/config/prompts.py`

## Testing Strategy

```
Unit Tests
    ├── src/utils/code_utils.py
    ├── src/utils/visualization_handler.py
    └── src/agents/response_processor.py

Integration Tests
    ├── Agent + LLM communication
    ├── Tool integration
    └── End-to-end chat flow

UI Tests
    └── Streamlit app interactions
```

## Deployment Considerations

1. **Environment Variables**: API keys via env vars
2. **Dependencies**: Listed in requirements.txt
3. **File Permissions**: Temp file cleanup
4. **Port Configuration**: Default Streamlit port 8501
