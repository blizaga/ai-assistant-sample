import streamlit as st
from services.llm_routers import get_llm, get_available_providers
from config.llm_config import CONFIG

st.title("SEO Text Generator")

available_providers = get_available_providers()
if not available_providers:
    st.error("No LLM providers configured. Please add API keys in your secrets.toml file.")
    st.stop()

provider = st.selectbox("Choose LLM Provider", available_providers)

title = st.text_input("Enter title...")

if st.button("Generate") and title:
    with st.spinner(f"Generating SEO content using {provider}..."):
        llm = get_llm(provider)
        prompt = f"""
        You are an expert SEO content writer for e-commerce.
        
        Using the product title: "{title}", generate the following structured SEO content:
        
        1. **Product Title**  
           - A unique, SEO-optimized title for this product.
        
        2. **Product Description**  
           - Persuasive and informative, suitable for a webshop product page.
           - Do not use the word "Empire".
        
        3. **Historical Information**  
           - Concise historical context related to the product or its origin.
        
        4. **Brief Product Description**  
           - A short version for category listings.
        
        5. **Image Metadata**  
           - For 5 product images, provide:
             - Alt text (SEO-relevant)
             - Image title (use underscores: e.g. product_name_detail.jpg)
             - Caption (1 sentence)
             - Description (2-3 sentences, SEO-rich)
        
        6. **Google SEO Snippets**
           - Meta Title (max 70 characters)
           - Meta Description (max 160 characters)
        
        All content must be SEO-friendly, engaging, and written in natural language.
        """

        response = llm.invoke(prompt)
        st.write("**SEO Content:**", response.content)