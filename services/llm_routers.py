from langchain.chat_models import ChatOpenAI
from langchain.llms import Ollama
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from config.llm_config import CONFIG

def get_available_providers():
    """Return a list of providers that have API keys configured."""
    available = []
    for provider, cfg in CONFIG.items():
        # For most providers, check if API key exists and is not empty
        if provider != "ollama" and cfg.get("api_key"):
            available.append(provider)
        # For Ollama, check if host is configured
        elif provider == "ollama" and cfg.get("host"):
            available.append(provider)
    return available

def get_llm(provider: str, streaming=False, callbacks=None):
    cfg = CONFIG.get(provider)
    if provider == "openai":
        return ChatOpenAI(
            api_key=cfg["api_key"], 
            model_name=cfg["model"],
            streaming=streaming, 
            callbacks=callbacks
        )
    elif provider == "anthropic":
        return ChatAnthropic(
            api_key=cfg["api_key"], 
            model=cfg["model"],
            streaming=streaming, 
            callbacks=callbacks
        )
    elif provider == "gemini":
        # For Gemini, streaming is passed differently
        return ChatGoogleGenerativeAI(
            google_api_key=cfg["api_key"], 
            model=cfg["model"],
            convert_system_message_to_human=True,
            callbacks=callbacks,
            stream=streaming  # Use stream parameter instead of streaming
        )
    elif provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(
            api_key=cfg["api_key"], 
            model=cfg["model"],
            streaming=streaming, 
            callbacks=callbacks
        )
    elif provider == "ollama":
        return Ollama(
            base_url=cfg["host"], 
            model=cfg["model"],
            callbacks=callbacks
        )
    else:
        raise ValueError("Unsupported provider")