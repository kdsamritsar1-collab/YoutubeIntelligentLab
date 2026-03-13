import streamlit as st
import google.generativeai as genai
from model_utils import get_active_gemini_model  # हमारी नई फाइल से इम्पोर्ट करें

# ... (बाकी API Setup वाला हिस्सा यहाँ रहेगा) ...

if st.button("Clone with AI SEO"):
    with st.spinner('Detecting active model and analyzing content...'):
        try:
            # ऑटो-डिटेक्ट फंक्शन को कॉल करें
            active_model_name = get_active_gemini_model()
            
            # उस मॉडल के साथ Gemini शुरू करें
            model = genai.GenerativeModel(active_model_name)
            
            # बाकी का AI Prompt और Generation लॉजिक यहाँ आएगा
            # response = model.generate_content(ai_prompt)
            
            st.success(f"Running on model: {active_model_name}")
            
        except Exception as e:
            st.error(f"Process Error: {e}")
