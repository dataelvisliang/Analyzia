"""
Analyzia - AI-Powered Data Analysis Platform
Main application entry point
"""

import streamlit as st
import pandas as pd
from tempfile import NamedTemporaryFile

from src.agents import DataAnalysisAgent, ResponseProcessor
from src.utils import DataFrameUtils
from src.config import AVAILABLE_MODELS


class DataApp:
    """Main application class that orchestrates all components"""

    def __init__(self):
        self.df = None
        self.file_path = None
        self.response_processor = None
        self.analysis_agent = None

    def process_uploaded_file(self, file, openrouter_api_key=None, model=None):
        """Process the uploaded CSV file and return dataframe and file path."""
        with st.spinner("Loading dataset..."):
            try:
                # Create temporary file
                with NamedTemporaryFile(delete=False) as f:
                    f.write(file.getbuffer())
                    self.file_path = f.name

                # Load dataframe with error handling
                try:
                    self.df = pd.read_csv(self.file_path)
                except Exception as e:
                    st.error(f"Error reading CSV file: {str(e)}")
                    st.info("Make sure your file is a valid CSV with proper formatting.")
                    return None

                # Initialize components
                self.response_processor = ResponseProcessor(self.df)
                self.analysis_agent = DataAnalysisAgent(self.df, self.response_processor, openrouter_api_key, model)

                return self.df

            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
                return None

    def configure_page(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="Analyzia - AI Data Analysis",
            page_icon="🤖",
            layout="centered",
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'https://github.com/ahammadnafiz/Analyzia',
                'Report a bug': 'https://github.com/ahammadnafiz/Analyzia/issues',
                'About': "Analyzia - AI-Powered Data Analysis Platform"
            }
        )

    def apply_custom_css(self):
        """Apply custom CSS for better UI"""
        st.markdown("""
        <style>
        /* Hide Streamlit branding but keep essential elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display: none;}

        /* Keep header visible but hide only the GitHub icon and deploy button */
        header[data-testid="stHeader"] {
            background-color: transparent;
        }

        /* Ensure sidebar remains visible and functional */
        .css-1d391kg {display: block !important;}
        section[data-testid="stSidebar"] {
            display: block !important;
            visibility: visible !important;
        }

        /* Main content area */
        .main .block-container {
            padding-top: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 800px;
        }

        /* Chat message styling */
        .stChatMessage {
            background-color: transparent;
            border: none;
        }

        /* Chat input styling - control width */
        .stChatInputContainer {
            max-width: 800px;
            margin: 0 auto;
        }

        /* Fixed chat input container */
        div[data-testid="stChatInputContainer"] {
            max-width: 800px !important;
            margin: 0 auto !important;
            padding: 0 1rem;
        }

        /* Chat input field styling */
        div[data-testid="stChatInputContainer"] > div {
            max-width: 100% !important;
        }

        /* Ensure sidebar toggle button is visible */
        button[data-testid="collapsedControl"] {
            display: block !important;
            visibility: visible !important;
        }
        </style>
        """, unsafe_allow_html=True)

    def render_sidebar(self):
        """Render the sidebar with configuration options"""
        with st.sidebar:
            # Additional sidebar styling
            st.markdown("""
            <style>
            /* Additional sidebar styling to ensure visibility */
            .css-1lcbmhc.e1fqkh3o0 {
                width: 250px !important;
                min-width: 250px !important;
            }

            /* Sidebar content styling */
            .css-17eq0hr {
                padding: 1rem;
            }
            </style>
            """, unsafe_allow_html=True)

            st.markdown("# 🤖 Analyzia")
            st.markdown("*AI-Powered Data Analysis*")
            st.markdown("---")

            # API Key section
            st.markdown("### 🔑 API Configuration")
            openrouter_api_key = st.text_input(
                "OpenRouter API Key",
                type="password",
                placeholder="Enter your API key...",
                help="Get your API key from https://openrouter.ai/keys"
            )

            # Model selection
            st.markdown("### 🤖 Model Selection")
            selected_model = st.selectbox(
                "Choose AI Model",
                AVAILABLE_MODELS,
                help="Select the AI model for data analysis. If one model is rate-limited, try another."
            )

            # Rate limit info
            st.caption("💡 All models are free. Try different ones if you encounter rate limits.")

            st.markdown("---")

            # File upload section
            st.markdown("### 📁 Data Upload")
            uploaded_file = st.file_uploader("Choose CSV file", type=["csv"], label_visibility="collapsed")

            return openrouter_api_key, selected_model, uploaded_file

    def render_header(self):
        """Render the main header"""
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0 2rem 0;">
            <h1 style="margin-bottom: 0.5rem; font-size: 3rem; font-weight: bold;">Analyzia</h1>
            <p style="color: #666; font-size: 1.1rem; margin: 0;">
                AI-Powered Data Analysis Platform
            </p>
        </div>
        """, unsafe_allow_html=True)

    def render_status_messages(self, uploaded_file, openrouter_api_key):
        """Render status messages based on app state"""
        if not uploaded_file and not openrouter_api_key:
            st.markdown("""
            <div style="text-align: center; padding: 1rem 0;">
                <p style="color: #0066cc; background-color: #e6f3ff; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #0066cc; margin: 0 auto; max-width: 600px;">
                👈 Get started by uploading a file and entering your API key in the sidebar
                </p>
            </div>
            """, unsafe_allow_html=True)
        elif not uploaded_file:
            st.markdown("""
            <div style="text-align: center; padding: 1rem 0;">
                <p style="color: #0066cc; background-color: #e6f3ff; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #0066cc; margin: 0 auto; max-width: 600px;">
                    📁 Please upload a CSV file in the sidebar to get started.
                </p>
            </div>
            """, unsafe_allow_html=True)
        elif not openrouter_api_key:
            st.markdown("""
            <div style="text-align: center; padding: 1rem 0;">
                <p style="color: #0066cc; background-color: #e6f3ff; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #0066cc; margin: 0 auto; max-width: 600px;">
                    🔑 Please enter your OpenRouter API key in the sidebar to start analyzing your data.
                </p>
            </div>
            """, unsafe_allow_html=True)

    def handle_chat_interaction(self, prompt, uploaded_file, openrouter_api_key):
        """Handle chat interactions with validation"""
        if not uploaded_file:
            response = """
🚫 **No Dataset Found**

I'd love to help you analyze your data, but I don't see any dataset uploaded yet.

**To get started:**
1. 📁 Upload a CSV file using the sidebar
2. 🔑 Enter your OpenRouter API key in the sidebar
3. 🚀 Ask your question again

Once you've uploaded your data, I can help you with:
- Data exploration and summaries
- Statistical analysis and correlations
- Beautiful visualizations and charts
- Business insights and recommendations
            """
            st.markdown(response)
            return response

        elif not openrouter_api_key:
            response = """
🔑 **API Key Required**

I can see your dataset, but I need an OpenRouter API key to analyze it for you.

**To continue:**
1. 🔑 Enter your OpenRouter API key in the sidebar (get one from https://openrouter.ai/keys)
2. 🚀 Ask your question again

Your data is ready - I just need the API key to start the analysis!
            """
            st.markdown(response)
            return response

        elif self.analysis_agent and self.analysis_agent.agent:
            # Everything is set up - proceed with analysis
            response = self.analysis_agent.handle_chat_input(prompt)
            return response

        else:
            response = """
⚠️ **Setup Issue**

There seems to be an issue with the analysis setup. Please try:

1. 🔄 Refresh the page
2. 📁 Re-upload your CSV file
3. 🔑 Re-enter your API key
4. 🚀 Ask your question again

If the problem persists, please check that your API key is valid and your CSV file is properly formatted.
            """
            st.markdown(response)
            return response

    def run(self):
        """Run the main application"""
        # Configure page
        self.configure_page()
        self.apply_custom_css()

        # Render sidebar and get inputs
        openrouter_api_key, selected_model, uploaded_file = self.render_sidebar()

        # Initialize or reset session state if needed
        if 'messages' not in st.session_state:
            st.session_state.messages = []

        # Process file if uploaded
        if uploaded_file and (self.df is None or uploaded_file.name != getattr(st.session_state, 'last_file', None)):
            self.process_uploaded_file(uploaded_file, openrouter_api_key, selected_model)
            st.session_state.last_file = uploaded_file.name if self.df is not None else None

            # Reset chat history when new file is uploaded
            st.session_state.messages = []

        # Setup agent if conditions are met
        if self.df is not None and openrouter_api_key:
            if self.analysis_agent and self.analysis_agent.agent is None:
                # Update API key and model if changed
                self.analysis_agent.openrouter_api_key = openrouter_api_key
                self.analysis_agent.model = selected_model
                self.analysis_agent.setup_agent(self.file_path)

        # Render header
        self.render_header()

        # Show dataset overview if dataset is uploaded
        if self.df is not None:
            DataFrameUtils.display_dataframe_info(self.df)

        # Display status information if setup is incomplete
        self.render_status_messages(uploaded_file, openrouter_api_key)

        # Chat messages container
        chat_container = st.container()

        with chat_container:
            # Display chat messages
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # Chat input - always visible at bottom
        if prompt := st.chat_input("Ask me anything about your data..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)

            # Display assistant response with validation
            with st.chat_message("assistant"):
                response = self.handle_chat_interaction(prompt, uploaded_file, openrouter_api_key)
                st.session_state.messages.append({"role": "assistant", "content": response})


# Run the application
if __name__ == "__main__":
    app = DataApp()
    app.run()
