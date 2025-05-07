import streamlit as st

CONFIG = {
    "openai": {
        "api_key": st.secrets["OPENAI_API_KEY"],
        "model": "gpt-4"
    },
    "anthropic": {
        "api_key": st.secrets["ANTHROPIC_API_KEY"],
        "model": "claude-3-opus-20240229"
    },
    "gemini": {
        "api_key": st.secrets["GOOGLE_API_KEY"],
        "model": "gemini-2.0-flash"
    },
    "groq": {
        "api_key": st.secrets["GROQ_API_KEY"],
        "model": "mixtral-8x7b-32768"
    },
    "ollama": {
        "host": st.secrets["OLLAMA_HOST"],
        "model": "mistral"
    }
}
