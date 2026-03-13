import streamlit as st
from googleapiclient.discovery import build
from pytrends.request import TrendReq
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import pandas as pd
import plotly.express as px
import time
import random

# 1. Page Configuration & Custom CSS
st.set_page_config(page_title="Ruhani YouTube Lab", layout="wide", page_icon="📈")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1, h2, h3 { color: #FFD700; text-align: center; }
    .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 20px; }
    .stTabs [data-baseweb="tab"] { background-color: rgba(255, 215, 0, 0.1); border-radius: 10px; padding: 10px 20px; }
    .stCode { background-color: #1a1c23 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. API Configuration (using Streamlit Secrets)
try:
    YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    
    # YouTube API Setup
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    
    # Gemini AI Setup
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as e:
    st.error(f"API Key Error: {e}. Please check Streamlit Secrets.")

# Google Trends Setup
pytrends = TrendReq(hl='en-US', tz=360)

# 3. Header & Sidebar
st.title("☬ Ruhani YouTube Intelligence Lab")
st.sidebar.title("Control Room")
niche = st.sidebar.selectbox("Channel Niche:", ["Sikh Devotional", "Punjabi Music", "Educational"])

# 4. Main Navigation Tabs
tab1, tab2, tab3 = st.tabs(["🚀 AI SEO Extractor", "📈 Market Trends", "📅 Smart Scheduler"])

# --- TAB 1: AI SEO Extractor (Fully Gemini-Powered) ---
with tab1:
    st.header("🚀 Advanced AI SEO Extractor")
    
    # Requirement: Ask for Channel Name
    my_channel_name = st.text_input("YOUR Channel Name:", value="Ruhani Jot")
    viral_url = st.text_input("Paste Trending Video URL:", placeholder="https://www.youtube.com/watch?v=...")

    if st.button("Clone with AI SEO"):
        if "v=" in viral_url:
            with st.spinner('Analyzing viral content with Gemini AI...'):
                try:
                    # a. Fetch Video Data using YouTube API
                    video_id = viral_url.split("v=")[1].split("&")[0]
                    req = youtube.videos().list(part="snippet,statistics", id=video_id).execute()
                    item = req['items'][0]
                    
                    viral_title = item['snippet']['title']
                    viral_desc = item['snippet']['description']
                    viral_tags = item['snippet'].get('tags', [])
                    
                    # b. Fetch Transcript
                    try:
                        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['pa', 'hi', 'en'])
                        full_transcript = " ".join([t['text'] for t in transcript_list])
                    except:
                        full_transcript = "Not Available"

                    st.divider()

                    # c. Initialize Gemini Model
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # d. AI Prompt Engineering
                    ai_prompt = f"""
                    You are a world-class YouTube SEO expert. Your goal is to reverse-engineer a viral devotional video's metadata for a new, copyright-safe video on the channel '{my_channel_name}'.

                    INPUT DATA FROM VIRAL VIDEO:
                    - Title: {viral_title}
                    - Description: {viral_desc}
                    - Tags: {', '.join(viral_tags)}
                    - Transcript/Lyrics: {full_transcript}

                    YOUR TASK (using pure Gurmukhi for lyrics, and English for SEO):
                    1. (Output 1) Provide the exact Gurmukhi transcript (lyrics) for the song. If not available, state 'Unavailable'.
                    2. (Output 2) Create 1 Highly Optimized, Unique Title for OUR new video. It must include core keywords from the viral title, remove original channel name, and end with "| {my_channel_name}". Ensure natural keyword flow.
                    3. (Output 3) Write a Professional, Copyright-Safe Description for OUR video. Do NOT copy the viral description word-for-word. Instead, naturally "clone" the key keywords and context (praise, spiritual theme, Gurbani relevance) into a unique, coherent narrative. Integrate Google Trends insights (assume topics like Gurbani and Simran are trending). Avoid copyright issues.
                    4. (Output 4) Provide a comma-separated list of 15 trending tags, combining the best viral tags and unique tags for {my_channel_name}.

                    Structure the final output clearly with these markers: [TRANSCRIPT], [TITLE], [DESCRIPTION], [TAGS].
                    """

                    # e. Generate AI Response
                    response = model.generate_content(ai_prompt)
                    full_ai_output = response.text

                    # f. Parse and Display Output
                    if "[TRANSCRIPT]" in full_ai_output and "[DESCRIPTION]" in full_ai_output:
                        try:
                            # अलग-अलग सेक्शन में डेटा विभाजित करना
                            transcript_data = full_ai_output.split("[TRANSCRIPT]")[1].split("[TITLE]")[0].strip()
                            title_data = full_ai_output.split("[TITLE]")[1].split("[DESCRIPTION]")[0].strip()
                            desc_data = full_ai_output.split("[DESCRIPTION]")[1].split("[TAGS]")[0].strip()
                            tags_data = full_ai_output.split("[TAGS]")[1].strip()
                            
                            tab_in_1, tab_in_2 = st.tabs(["📝 Transcript & Lyrics", "📈 Optimized SEO"])
                            
                            with tab_in_1:
                                st.subheader("Lyrics (Gurmukhi)")
                                st.text_area("Original Video Transcript:", transcript_data, height=300)
                            
                            with tab_in_2:
                                st.subheader("Viral Tag Analysis")
                                st.code(", ".join(viral_tags))
                                st.info("AI Tip: Gemini has integrated these keywords naturally into your new description.")
                                
                                st.subheader("Your AI-Optimized Video Title")
                                st.code(title_data)
                                
                                st.subheader("Your AI-Optimized Video Description (Copyright Safe)")
                                st.code(desc_data)
                                
                                st.subheader("Suggested SEO Tags")
                                st.code(tags_data)
                                
                            st.success("✅ SEO Assets Created by Gemini AI!")
                        
                        except Exception as e:
                            st.error(f"Error parsing AI output: {e}")
                    else:
                        st.code(full_ai_output) # Fallback if markers are missing

                except Exception as e:
                    st.error(f"YouTube Error: {e}")
        else:
            st.error("Invalid YouTube URL.")

# --- TAB 2 & 3: Market Trends & Scheduler (Same as previous safe logic) ---
with tab2:
    st.header("Google Trends Forecast")
    
    @st.cache_data(ttl=3600)
    def fetch_trending_data(topic):
        try:
            time.sleep(random.uniform(1, 3))
            pytrends.build_payload([topic], timeframe='today 12-m', geo='IN', gprop='youtube')
            return pytrends.interest_over_time()
        except:
            return "LIMIT_ERROR"

    if st.button("Check Trend Strength"):
        df = fetch_trending_data(niche)
        if isinstance(df, pd.DataFrame) and not df.empty:
            fig = px.line(df, y=niche, template="plotly_dark")
            fig.update_traces(line_color='#FFD700', line_width=3)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Google Trends is busy or no data found. Please try again.")

st.markdown("---")
st.markdown("<center>Designed for <b>@ruhanijot</b> | Powered by Gemini AI</center>", unsafe_allow_html=True)
