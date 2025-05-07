import streamlit as st

st.set_page_config(page_title="AI Assistant", layout="wide")
st.sidebar.title("AI Assistant")
st.sidebar.page_link("pages/1_chat_room.py", label="Chat Room")
st.sidebar.page_link("pages/2_seo_prompt.py", label="SEO Prompt")
