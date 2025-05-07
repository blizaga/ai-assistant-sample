import streamlit as st
from services.llm_routers import get_llm, get_available_providers
from config.llm_config import CONFIG
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.callbacks.base import BaseCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# Custom streaming handler for Streamlit
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text
        self.run_id = None
        
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

# Initialize chat history and other session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
if "conversation_memory" not in st.session_state:
    st.session_state.conversation_memory = ConversationBufferMemory()
    
if "processing" not in st.session_state:
    st.session_state.processing = False

if "current_response" not in st.session_state:
    st.session_state.current_response = ""

st.title("Chat Room")

# Display provider selection in sidebar
with st.sidebar:
    st.subheader("Model Settings")
    available_providers = get_available_providers()
    if not available_providers:
        st.error("No LLM providers configured. Please add API keys in your secrets.toml file.")
        st.stop()
    
    provider = st.selectbox("Choose LLM Provider", available_providers)
    
    # Add system message option
    system_message = st.text_area(
        "System Message (AI Assistant's Persona)", 
        value="You are a helpful AI assistant. Be concise, friendly, and provide accurate information.",
        help="Set the AI's behavior and personality"
    )
    
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.conversation_memory = ConversationBufferMemory()
        st.session_state.current_response = ""
        st.session_state.processing = False
        st.rerun()

# Display existing chat messages
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    else:
        with st.chat_message("assistant"):
            st.markdown(message.content)

# Handle user input
prompt = st.chat_input("Type your message here...", disabled=st.session_state.processing)
if prompt and not st.session_state.processing:
    # Set processing flag to prevent multiple submissions
    st.session_state.processing = True
    
    # Add user message to chat history and display it
    st.session_state.chat_history.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response in the assistant container
    with st.chat_message("assistant"):
        response_container = st.empty()
        
        # Define callback function to update session state
        def on_llm_token(token):
            st.session_state.current_response += token
            response_container.markdown(st.session_state.current_response)
        
        # Create a custom handler that updates session state
        class SessionStateHandler(BaseCallbackHandler):
            def on_llm_new_token(self, token: str, **kwargs) -> None:
                on_llm_token(token)
        
        # Generate the response using conversation memory
        with st.spinner("Thinking..."):
            llm = get_llm(provider, streaming=True, callbacks=[SessionStateHandler()])
            
            # Format messages for the model
            messages = []
            
            # Add system message if provided
            if system_message:
                messages.append(SystemMessage(content=system_message))
            
            # Add chat history for context
            for msg in st.session_state.chat_history:
                messages.append(msg)
            
            # Get response from LLM with full conversation context
            response = llm.invoke(messages)
            
            # Update conversation memory
            st.session_state.conversation_memory.save_context(
                {"input": prompt},
                {"output": response.content}
            )
            
            # Add completed AI message to chat history
            st.session_state.chat_history.append(AIMessage(content=response.content))
            
            # Reset for next interaction
            st.session_state.current_response = ""
            st.session_state.processing = False
            
            # Force a rerun to update the UI with completed state
            st.rerun()