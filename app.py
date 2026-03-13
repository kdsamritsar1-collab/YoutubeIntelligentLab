import streamlit as st
from googleapiclient.discovery import build
from pytrends.request import TrendReq
import pandas as pd
import plotly.express as px

# 1. Page Configuration & Aesthetic Style
st.set_page_config(page_title="Ruhani YouTube Lab", layout="wide", page_icon="📈")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; border-radius: 10px 10px 0px 0px; font-weight: bold; }
    .metric-box { background: rgba(255, 255, 255, 0.05); border: 1px solid #FFD700; border-radius: 15px; padding: 20px; text-align: center; }
    h1, h2, h3 { color: #FFD700; }
    </style>
    """, unsafe_allow_html=True)

# 2. API Setup (using Streamlit Secrets)
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
pytrends = TrendReq(hl='en-US', tz=360)

# 3. Sidebar
st.sidebar.title("☬ Ruhani Lab v2.0")
st.sidebar.info("YouTube Market Intelligence Tool for @ruhanijot")

# 4. Main Interface with Tabs
tab1, tab2, tab3 = st.tabs(["🔍 Competitor Analysis", "🚀 SEO Cloner", "📈 Niche Trends"])

# --- TAB 1: Competitor Analysis ---
with tab1:
    st.header("Competitor Channel Analysis")
    target_channel = st.text_input("Enter Competitor Channel ID or Video Link:")
    
    if st.button("Run Intelligence Report"):
        st.success("Analyzing top performing videos in your niche...")
        # Demo Data for UI - In production, this uses youtube.search().list()
        data = {"Video Title": ["Gurbani Kirtan 2026", "History of Sikhs", "Daily Simran"], "Views": ["500K", "1.2M", "300K"]}
        st.table(pd.DataFrame(data))

# --- TAB 2: SEO Cloner ---
with tab2:
    st.header("Viral Video SEO Extractor")
    viral_url = st.text_input("Paste Trending Video URL:")
    
    if st.button("Extract & Optimize SEO"):
        if "v=" in viral_url:
            video_id = viral_url.split("v=")[1].split("&")[0]
            req = youtube.videos().list(part="snippet,statistics", id=video_id).execute()
            item = req['items'][0]
            
            st.subheader("Extracted Metadata")
            st.write(f"**Viral Title:** {item['snippet']['title']}")
            tags = item['snippet'].get('tags', ["No tags found"])
            st.code(", ".join(tags))
            
            st.info("💡 Copy these tags to get into 'Suggested Videos' of this viral hit.")
        else:
            st.error("Invalid URL. Please use a full YouTube link.")

# --- TAB 3: Niche Trends ---
with tab3:
    st.header("Google Trends for YouTube")
    niche = st.selectbox("Your Niche:", ["Sikh Devotional", "Punjabi Music", "Educational", "Kids"])
    
    if st.button("Forecast Market"):
        pytrends.build_payload([niche], timeframe='today 12-m', geo='IN', gprop='youtube')
        df = pytrends.interest_over_time()
        
        if not df.empty:
            fig = px.line(df, y=niche, title=f"Interest Trend for {niche}", line_shape="spline")
            fig.update_traces(line_color='#FFD700')
            st.plotly_chart(fig, use_container_width=True)
            st.write("Best time to post: When the graph shows a peak.")