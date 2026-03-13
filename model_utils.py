import google.generativeai as genai
import streamlit as st

def get_active_gemini_model():
    """
    स्वचालित रूप से उपलब्ध सबसे सटीक Gemini मॉडल का पता लगाता है।
    """
    try:
        # उपलब्ध मॉडल्स की लिस्ट प्राप्त करें
        available_models = [
            m.name for m in genai.list_models() 
            if 'generateContent' in m.supported_generation_methods
        ]
        
        # 1. पहले 'gemini-1.5-flash' ढूँढें (जो सबसे तेज़ है)
        for m in available_models:
            if "gemini-1.5-flash" in m.lower():
                return m
        
        # 2. अगर फ्लैश नहीं मिला, तो कोई भी 'gemini' मॉडल चुनें
        for m in available_models:
            if "gemini" in m.lower():
                return m
                
        # 3. यदि कुछ भी नहीं मिलता, तो पुराना बैकअप
        return "models/gemini-1.5-flash"
        
    except Exception as e:
        st.error(f"Error detecting models: {e}")
        return "models/gemini-1.5-flash" # Default Fallback