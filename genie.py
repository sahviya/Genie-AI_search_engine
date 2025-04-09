import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from openai import OpenAI
import time

# Set page config
st.set_page_config(
    page_title="Genie - AI Search Engine",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        :root {
            --primary: #6a35ff;
            --secondary: #ff6b35;
            --background: #ffffff;
            --text: #2d3748;
            --card-bg: #f8f9fa;
        }

        [data-theme="dark"] {
            --primary: #8a63ff;
            --secondary: #ff8c63;
            --background: #0e1117;
            --text: #f8f9fa;
            --card-bg: #1e1e1e;
        }

        .stTabs [role="tablist"] {
            justify-content: center;
            margin-bottom: 1rem;
        }

        .stTabs [role="tab"] {
            padding: 0.5rem 1rem;
            border-radius: 8px 8px 0 0;
            margin: 0 0.2rem;
            transition: all 0.3s;
        }

        .stTabs [role="tab"][aria-selected="true"] {
            background: var(--primary);
            color: white !important;
        }

        .stTabs [role="tab"]:not([aria-selected="true"]):hover {
            background: rgba(106, 53, 255, 0.1);
        }

        .video-container {
            position: relative;
            padding-bottom: 56.25%;
            height: 0;
            overflow: hidden;
            border-radius: 12px;
            margin-bottom: 1rem;
        }

        .video-container iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar settings
with st.sidebar:
    st.title("Genie Settings")
    with st.expander("API Keys"):
        openai_key = st.text_input("OpenAI Key:", type="password")
        google_api_key = st.text_input("Google API Key:", type="password")
        search_engine_id = st.text_input("Search Engine ID:")
        youtube_api_key = st.text_input("YouTube API Key:", type="password")

    with st.expander("Search Options"):
        num_results = st.slider("Results per tab:", 1, 10, 3)
        ai_enabled = st.checkbox("Enable AI Answers", True)
        safe_search = st.checkbox("Safe Search", True)

# Main header
st.markdown("""
    <div style="text-align:center; background:linear-gradient(135deg, var(--primary), var(--secondary));
                color:white; padding:1.5rem; border-radius:12px; margin-bottom:1.5rem;">
        <h1 style="margin:0;">Genie</h1>
        <p style="margin:0; opacity:0.9;">Your AI-powered search companion</p>
    </div>
""", unsafe_allow_html=True)

# Search form
with st.form(key='search_form'):
    query = st.text_input("", placeholder="Ask Genie anything...", label_visibility="collapsed")
    search_btn = st.form_submit_button("Search", use_container_width=True)

# Session state initialization
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Web"
if 'search_data' not in st.session_state:
    st.session_state.search_data = {"Web": None, "Images": None, "Videos": None}
if 'ai_answer' not in st.session_state:
    st.session_state.ai_answer = None

# Search functions
def google_search(query, api_key, engine_id, num=3, safe=True):
    try:
        safe_setting = "active" if safe else "off"
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={engine_id}&num={num}&safe={safe_setting}"
        response = requests.get(url).json()
        return [{
            'title': item.get('title'),
            'link': item.get('link'),
            'snippet': item.get('snippet'),
            'meta': item.get('pagemap', {}).get('metatags', [{}])[0]
        } for item in response.get('items', [])]
    except Exception as e:
        st.error(f"Search error: {str(e)}")
        return []

def google_image_search(query, api_key, engine_id, num=6, safe=True):
    try:
        safe_setting = "active" if safe else "off"
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={engine_id}&searchType=image&num={num}&safe={safe_setting}"
        response = requests.get(url).json()
        return [{
            'title': item.get('title'),
            'link': item.get('link'),
            'thumbnail': item.get('image', {}).get('thumbnailLink'),
            'context': item.get('snippet')
        } for item in response.get('items', [])]
    except Exception as e:
        st.error(f"Image search error: {str(e)}")
        return []

def youtube_search(query, api_key, num=3):
    try:
        url = f"https://www.googleapis.com/youtube/v3/search?q={query}&key={api_key}&part=snippet&maxResults={num}&type=video"
        response = requests.get(url).json()
        return [{
            'title': item['snippet']['title'],
            'videoId': item['id']['videoId'],
            'thumbnail': item['snippet']['thumbnails']['high']['url'],
            'channel': item['snippet']['channelTitle']
        } for item in response.get('items', [])]
    except Exception as e:
        st.error(f"Video search error: {str(e)}")
        return []

def get_ai_answer(query, api_key):
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Genie, a helpful AI. Provide concise, accurate answers with bullet points when helpful."},
                {"role": "user", "content": query}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"AI error: {str(e)}")
        return None

# Process search
if search_btn and query:
    if not google_api_key or not search_engine_id:
        st.warning("Please provide all required API keys")
    else:
        with st.spinner("Genie is gathering knowledge..."):
            start_time = time.time()
            st.session_state.search_data["Web"] = google_search(query, google_api_key, search_engine_id, num_results, safe_search)
            st.session_state.search_data["Images"] = google_image_search(query, google_api_key, search_engine_id, num_results * 2, safe_search)
            if youtube_api_key:
                st.session_state.search_data["Videos"] = youtube_search(query, youtube_api_key, num_results)
            if ai_enabled and openai_key:
                st.session_state.ai_answer = get_ai_answer(query, openai_key)
            st.session_state.search_time = round(time.time() - start_time, 2)

# Tabs
tabs = st.tabs(["Web", "Images", "Videos"])

with tabs[0]:
    if st.session_state.search_data["Web"]:
        st.caption(f"Found {len(st.session_state.search_data['Web'])} web results in {st.session_state.search_time}s")
        if st.session_state.ai_answer:
            with st.expander("AI Summary", expanded=True):
                st.markdown(st.session_state.ai_answer)
        for result in st.session_state.search_data["Web"]:
            with st.container():
                st.markdown(f"### [{result['title']}]({result['link']})")
                st.caption(result['link'])
                if result.get('snippet'):
                    st.markdown(result['snippet'])
                if result.get('meta', {}).get('og:description'):
                    st.markdown(f"*{result['meta']['og:description']}*")
                st.markdown("---")

with tabs[1]:
    if st.session_state.search_data["Images"]:
        st.caption(f"Found {len(st.session_state.search_data['Images'])} images in {st.session_state.search_time}s")
        cols = st.columns(3)
        for i, img in enumerate(st.session_state.search_data["Images"]):
            with cols[i % 3]:
                st.image(img['thumbnail'] or img['link'], use_container_width=True)
                if img['title'] and img['title'] != 'Image':
                    st.caption(img['title'][:50] + ("..." if len(img['title']) > 50 else ""))

with tabs[2]:
    if youtube_api_key:
        if st.session_state.search_data["Videos"]:
            st.caption(f"Found {len(st.session_state.search_data['Videos'])} videos in {st.session_state.search_time}s")
            for video in st.session_state.search_data["Videos"]:
                with st.container():
                    st.markdown(f"### {video['title']}")
                    st.markdown(f"""
                        <div class="video-container">
                            <iframe src="https://www.youtube.com/embed/{video['videoId']}" frameborder="0" allowfullscreen></iframe>
                        </div>
                    """, unsafe_allow_html=True)
                    st.caption(f"Channel: {video['channel']}")
                    st.markdown("---")
        else:
            st.info("No videos found. Try a different search query.")
    else:
        st.warning("YouTube API key not provided. Video search unavailable.")

# Empty state
if not query:
    st.markdown("""
    <div style="text-align:center; padding:3rem 0;">
        <p style="font-size:1.2rem; color:var(--text);">What knowledge do you seek today?</p>
        <p style="opacity:0.7; color:var(--text);">Genie is ready to reveal all answers...</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Genie • Your wish is my command • Powered by OpenAI, Google & YouTube")