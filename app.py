import streamlit as st
from googleapiclient.discovery import build
from pytrends.request import TrendReq
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import pandas as pd
import plotly.express as px
import time
import random

# model_utils.py से फंक्शन इम्पोर्ट करें
from model_utils import get_active_gemini_model

# --- Page Config ---
st.set_page_config(page_title="Ruhani YouTube Lab", layout="wide", page_icon="📈")

# --- API Setup ---
try:
    YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    genai.configure(api_key=GEMINI_API_KEY)
    pytrends = TrendReq(hl='en-US', tz=360)
except Exception as e:
    st.error("API Keys missing in Streamlit Secrets!")

# --- UI Header ---
st.markdown("<h1 style='text-align: center; color: #FFD700;'>☬ Ruhani YouTube Intelligence Lab</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🚀 AI SEO Extractor", "📈 Market Trends", "📅 Smart Scheduler"])

# --- TAB 1: AI SEO Extractor ---
with tab1:
    st.header("Viral SEO Extractor (Powered by Gemini)")
    
    my_channel_name = st.text_input("YOUR Channel Name:", value="Ruhani Jot")
    viral_url = st.text_input("Paste Trending Video URL:", placeholder="https://www.youtube.com/watch?v=...")

    if st.button("Clone & Optimize with AI"):
        if "v=" in viral_url:
            with st.spinner('Reverse-engineering viral strategy...'):
                try:
                    video_id = viral_url.split("v=")[1].split("&")[0]
                    
                    # 1. YouTube Data Fetch
                    v_req = youtube.videos().list(part="snippet,statistics", id=video_id).execute()
                    item = v_req['items'][0]
                    v_title = item['snippet']['title']
                    v_desc = item['snippet']['description']
                    v_tags = item['snippet'].get('tags', [])
                    
                    # 2. Transcript Fetch
                    try:
                        t_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['pa', 'hi', 'en'])
                        transcript = " ".join([t['text'] for t in t_list])
                    except:
                        transcript = "Transcript not available for this video."

                    # 3. Dynamic Model Detection
                    active_model = get_active_gemini_model()
                    model = genai.GenerativeModel(active_model)

                    # 4. Gemini AI Prompt
                    prompt = f"""
                    You are a world-class YouTube SEO expert. 
                    Original Title: {v_title}
                    Original Tags: {', '.join(v_tags)}
                    Original Description Snippet: {v_desc[:500]}
                    Song Transcript: {transcript}
                    My Channel Name: {my_channel_name}

                    Task:
                    1. [TRANSCRIPT]: Provide the full Gurmukhi lyrics/transcript.
                    2. [TITLE]: Create a viral, keyword-rich title for our video. It must end with '| {my_channel_name}'.
                    3. [DESCRIPTION]: Write a professional, unique, copyright-safe description. Clone the 'vibe' and keywords of the original video naturally. Include Google Trends insights for Sikh Devotional niche.
                    4. [TAGS]: Suggest 15 trending tags (comma separated).
                    """

                    response = model.generate_content(prompt)
                    output = response.text

                    # 5. Display Results
                    st.success(f"Using Model: {active_model}")
                    st.divider()
                    
                    # Simple parsing (assuming markers were used)
                    st.text_area("📜 Song Lyrics / Transcript", transcript, height=200)
                    st.subheader("🚀 Optimized SEO Package")
                    st.write(output)

                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.error("Please enter a valid YouTube URL.")

# --- Tab 2 & 3 (Trends & Scheduler) ---
# (इनमें आपका पुराना वर्किंग कोड रहेगा)

st.markdown("---")
st.markdown("<center>Ruhani Jot AI Ecosystem v2.0</center>", unsafe_allow_html=True)
