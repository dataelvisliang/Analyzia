"""DataFrame utility functions"""

import streamlit as st


class DataFrameUtils:
    """Utility class for dataframe operations"""

    @staticmethod
    def display_dataframe_info(df):
        """Display information about the dataframe."""
        st.markdown("<h3 style='text-align: center;'>Dataset Overview</h3>", unsafe_allow_html=True)
        # Show sample data in expander
        with st.expander("View sample data"):
            st.dataframe(df.head(), use_container_width=True)
