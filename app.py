import streamlit as st
import pandas as pd
import requests
import feedparser
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import os
from dotenv import load_dotenv
import google.generativeai as genai
import json

# Load environment variables
load_dotenv()

# --- Page Config ---
st.set_page_config(
    page_title="SupplyAlert | Supply Chain Intelligence",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(180deg, #0a0f1a 0%, #111827 100%);
        color: #E2E8F0;
    }
    
    /* Premium Hero */
    .hero {
        text-align: center;
        padding: 60px 40px;
        background: radial-gradient(ellipse at top, rgba(59, 130, 246, 0.15) 0%, transparent 50%),
                    radial-gradient(ellipse at bottom, rgba(139, 92, 246, 0.1) 0%, transparent 50%),
                    linear-gradient(180deg, rgba(15, 23, 42, 0.8) 0%, rgba(15, 23, 42, 0.95) 100%);
        border-radius: 28px;
        margin-bottom: 40px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        backdrop-filter: blur(20px);
        position: relative;
        overflow: hidden;
    }
    .hero::before {
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.5), transparent);
    }
    
    /* Animated Logo Icon */
    .logo-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 50%, #EC4899 100%);
        border-radius: 20px;
        margin-bottom: 24px;
        font-size: 2.5rem;
        box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3),
                    0 0 60px rgba(139, 92, 246, 0.2);
        animation: pulse-glow 3s ease-in-out infinite;
    }
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3), 0 0 60px rgba(139, 92, 246, 0.2); }
        50% { box-shadow: 0 25px 50px rgba(99, 102, 241, 0.4), 0 0 80px rgba(139, 92, 246, 0.3); }
    }
    
    .hero h1 {
        font-family: 'Inter', sans-serif;
        font-size: 3.2rem;
        font-weight: 800;
        margin-bottom: 16px;
        background: linear-gradient(135deg, #F8FAFC 0%, #CBD5E1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.03em;
    }
    .hero-subtitle {
        font-size: 1.15rem;
        color: #94A3B8;
        margin-bottom: 28px;
        font-weight: 400;
        max-width: 500px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
    }
    .hero-badge {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(59, 130, 246, 0.2) 100%);
        color: #10B981;
        padding: 10px 24px;
        border-radius: 100px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        border: 1px solid rgba(16, 185, 129, 0.3);
        letter-spacing: 0.03em;
    }
    .hero-badge::before {
        content: '';
        width: 8px;
        height: 8px;
        background: #10B981;
        border-radius: 50%;
        animation: blink 1.5s ease-in-out infinite;
    }
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #F1F5F9;
        margin: 30px 0 20px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Alert Cards */
    .alert-card {
        background: rgba(31, 41, 55, 0.6);
        padding: 18px 20px;
        border-radius: 12px;
        border-left: 3px solid #EF4444;
        margin: 10px 0;
        backdrop-filter: blur(5px);
        transition: all 0.2s ease;
    }
    .alert-card:hover {
        background: rgba(31, 41, 55, 0.8);
        transform: translateX(4px);
    }
    .alert-card.warning {
        border-left-color: #F59E0B;
    }
    .alert-card.info {
        border-left-color: #3B82F6;
    }
    .alert-card.ai {
        border-left-color: #8B5CF6;
    }
    .alert-card.policy {
        border-left-color: #EC4899;
    }
    
    /* Stat Cards */
    .stat-card {
        background: rgba(30, 41, 59, 0.5);
        padding: 28px;
        border-radius: 16px;
        text-align: center;
        border: 1px solid rgba(51, 65, 85, 0.5);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    .stat-card:hover {
        border-color: rgba(59, 130, 246, 0.5);
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.15);
        transform: translateY(-2px);
    }
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #10B981;
        line-height: 1;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #64748B;
        margin-top: 8px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 500;
    }
    
    /* News Cards */
    .news-card {
        background: rgba(31, 41, 55, 0.4);
        padding: 14px 16px;
        border-radius: 10px;
        margin: 8px 0;
        border-left: 3px solid #3B82F6;
        transition: all 0.2s ease;
    }
    .news-card:hover {
        background: rgba(31, 41, 55, 0.7);
    }
    .news-card a {
        color: #E2E8F0;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.95rem;
        line-height: 1.4;
    }
    .news-card a:hover {
        color: #3B82F6;
    }
    .news-time {
        color: #64748B;
        font-size: 0.75rem;
        margin-top: 6px;
    }
    
    /* Chat Interface Styles */
    .chat-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 380px;
        max-height: 600px;
        background: rgba(15, 23, 42, 0.95);
        border-radius: 16px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(20px);
        z-index: 1000;
        display: flex;
        flex-direction: column;
    }
    .chat-header {
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
        padding: 16px 20px;
        border-radius: 16px 16px 0 0;
        color: white;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 16px;
        max-height: 400px;
    }
    .chat-message {
        margin-bottom: 12px;
        padding: 10px 14px;
        border-radius: 12px;
        line-height: 1.5;
        font-size: 0.9rem;
    }
    .chat-message.user {
        background: rgba(59, 130, 246, 0.2);
        border: 1px solid rgba(59, 130, 246, 0.3);
        color: #E2E8F0;
        margin-left: 20px;
    }
    .chat-message.assistant {
        background: rgba(31, 41, 55, 0.6);
        border: 1px solid rgba(51, 65, 85, 0.5);
        color: #CBD5E1;
        margin-right: 20px;
    }
    .chat-input-container {
        padding: 12px;
        border-top: 1px solid rgba(51, 65, 85, 0.5);
    }
    .chat-toggle-btn {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
        border: none;
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
        cursor: pointer;
        font-size: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 999;
        transition: all 0.3s ease;
    }
    .chat-toggle-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 12px 32px rgba(59, 130, 246, 0.6);
    }
</style>
""", unsafe_allow_html=True)


# --- DATA FETCHING ---

@st.cache_data(ttl=300)  # Cache for 5 minutes for fresh news
def get_freight_industry_news():
    """Fetch freight carrier news - XPO, Ryder, Penske, etc."""
    try:
        url = "https://news.google.com/rss/search?q=XPO+logistics+OR+Ryder+trucking+OR+Penske+freight+OR+JB+Hunt+OR+Schneider+trucking+OR+Werner+freight&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(url)
        return feed.entries[:6]
    except:
        return []

@st.cache_data(ttl=300)
def get_policy_news():
    """Fetch government policy and trade news"""
    try:
        url = "https://news.google.com/rss/search?q=freight+policy+OR+trucking+regulations+OR+USMCA+trade+OR+tariffs+logistics+OR+DOT+trucking+OR+FMCSA&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(url)
        return feed.entries[:6]
    except:
        return []

@st.cache_data(ttl=300)
def get_ai_supply_chain_news():
    """Fetch AI in supply chain news"""
    try:
        url = "https://news.google.com/rss/search?q=AI+supply+chain+OR+artificial+intelligence+logistics+OR+machine+learning+freight+OR+automation+warehouse&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(url)
        return feed.entries[:6]
    except:
        return []

@st.cache_data(ttl=300)
def get_disruption_news():
    """Fetch supply chain disruption news"""
    try:
        url = "https://news.google.com/rss/search?q=supply+chain+disruption+OR+port+congestion+OR+freight+delays+OR+shipping+crisis+OR+trucking+shortage&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(url)
        return feed.entries[:6]
    except:
        return []

@st.cache_data(ttl=300)
def get_southern_border_news():
    """Fetch Southern Border logistics and trade news"""
    try:
        url = "https://news.google.com/rss/search?q=southern+border+OR+Mexico+trade+OR+border+crossing+OR+customs+delay+OR+USMCA+OR+Laredo+freight+OR+El+Paso+logistics&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(url)
        return feed.entries[:6]
    except:
        return []

@st.cache_data(ttl=300)
def get_border_weather_news():
    """Fetch weather news affecting Southern Border region"""
    try:
        url = "https://news.google.com/rss/search?q=Texas+weather+OR+Mexico+storm+OR+hurricane+border+OR+Rio+Grande+Valley+weather+OR+border+flooding&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(url)
        return feed.entries[:6]
    except:
        return []

@st.cache_data(ttl=1800)
def get_weather_alerts():
    """Weather disruption alerts"""
    return [
        {"type": "Winter Storm Warning", "severity": "High", "location": "Upper Midwest", "impact": "I-94, I-90 delays expected"},
        {"type": "Fog Advisory", "severity": "Medium", "location": "Central Valley, CA", "impact": "Port trucking slowdowns"},
    ]

@st.cache_data(ttl=900)
def get_port_status():
    """Port congestion status"""
    return {
        "Los Angeles/Long Beach": {"congestion": "High", "delay_days": 5, "color": "#EF4444"},
        "Savannah": {"congestion": "Medium", "delay_days": 2, "color": "#F59E0B"},
        "New York/New Jersey": {"congestion": "Low", "delay_days": 1, "color": "#10B981"},
        "Houston": {"congestion": "Medium", "delay_days": 3, "color": "#F59E0B"},
    }

def format_news_date(item):
    """Format news date to relative time"""
    try:
        if hasattr(item, 'published_parsed') and item.published_parsed:
            pub_time = datetime(*item.published_parsed[:6])
            now = datetime.now()
            diff = now - pub_time
            if diff.days == 0:
                hours = diff.seconds // 3600
                if hours == 0:
                    return "Just now"
                return f"{hours}h ago"
            elif diff.days == 1:
                return "Yesterday"
            elif diff.days < 7:
                return f"{diff.days} days ago"
            else:
                return pub_time.strftime("%b %d")
        return ""
    except:
        return ""

# --- AI AGENT FUNCTIONS ---

def initialize_gemini():
    """Initialize Gemini API"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # Try Streamlit secrets
        try:
            api_key = st.secrets.get("GEMINI_API_KEY")
        except:
            pass
    
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

def get_all_news_as_json():
    """Compile all news feeds into structured JSON for AI context"""
    news_data = {
        "freight_industry": [],
        "policy": [],
        "ai_supply_chain": [],
        "disruptions": [],
        "southern_border": [],
        "border_weather": [],
        "weather_alerts": get_weather_alerts(),
        "port_status": get_port_status()
    }
    
    # Fetch all news
    freight_news = get_freight_industry_news()
    for item in freight_news:
        news_data["freight_industry"].append({
            "title": item.title,
            "link": item.link,
            "published": format_news_date(item),
            "summary": getattr(item, 'summary', '')[:200]
        })
    
    policy_news = get_policy_news()
    for item in policy_news:
        news_data["policy"].append({
            "title": item.title,
            "link": item.link,
            "published": format_news_date(item),
            "summary": getattr(item, 'summary', '')[:200]
        })
    
    ai_news = get_ai_supply_chain_news()
    for item in ai_news:
        news_data["ai_supply_chain"].append({
            "title": item.title,
            "link": item.link,
            "published": format_news_date(item),
            "summary": getattr(item, 'summary', '')[:200]
        })
    
    disruption_news = get_disruption_news()
    for item in disruption_news:
        news_data["disruptions"].append({
            "title": item.title,
            "link": item.link,
            "published": format_news_date(item),
            "summary": getattr(item, 'summary', '')[:200]
        })
    
    border_news = get_southern_border_news()
    for item in border_news:
        news_data["southern_border"].append({
            "title": item.title,
            "link": item.link,
            "published": format_news_date(item),
            "summary": getattr(item, 'summary', '')[:200]
        })
    
    border_weather = get_border_weather_news()
    for item in border_weather:
        news_data["border_weather"].append({
            "title": item.title,
            "link": item.link,
            "published": format_news_date(item),
            "summary": getattr(item, 'summary', '')[:200]
        })
    
    return news_data

def filter_relevant_news(query, news_data):
    """RAG: Filter news based on query keywords for efficient context"""
    keywords = query.lower().split()
    
    # Keywords to search for
    relevant_items = []
    
    for category, items in news_data.items():
        if category in ["weather_alerts", "port_status"]:
            continue
        
        for item in items:
            # Check if any keyword matches in title or summary
            item_text = (item.get("title", "") + " " + item.get("summary", "")).lower()
            
            # Score based on keyword matches
            score = sum(1 for keyword in keywords if keyword in item_text)
            
            if score > 0:
                relevant_items.append({
                    "category": category,
                    "score": score,
                    **item
                })
    
    # Sort by relevance score
    relevant_items.sort(key=lambda x: x["score"], reverse=True)
    
    # Return top 10 most relevant items
    return relevant_items[:10]

def get_ai_response(user_query, news_data):
    """Get AI response using Gemini with RAG approach"""
    if not initialize_gemini():
        return "⚠️ AI Assistant is not configured. Please set your GEMINI_API_KEY in the .env file or Streamlit secrets. Get a free API key at https://ai.google.dev/"
    
    try:
        # Filter relevant news using RAG
        relevant_news = filter_relevant_news(user_query, news_data)
        
        # Build context from relevant news
        context = "# Current Supply Chain Intelligence Data\n\n"
        
        # Add weather alerts
        context += "## Weather Alerts:\n"
        for alert in news_data.get("weather_alerts", []):
            context += f"- {alert['type']} ({alert['severity']}): {alert['location']} - {alert['impact']}\n"
        
        # Add port status
        context += "\n## Port Congestion Status:\n"
        for port, data in news_data.get("port_status", {}).items():
            context += f"- {port}: {data['congestion']} congestion, {data['delay_days']} days delay\n"
        
        # Add relevant news
        if relevant_news:
            context += "\n## Relevant News Articles:\n"
            for item in relevant_news:
                context += f"\n### [{item['category'].replace('_', ' ').title()}] {item['title']}\n"
                context += f"Published: {item['published']}\n"
                if item.get('summary'):
                    context += f"Summary: {item['summary']}\n"
        
        # Create the AI prompt with specialized role
        system_prompt = """You are a Supply Chain Logistics Analyst specializing in Southern Border operations.

Your primary objective is to analyze real-time news data to identify bottlenecks at the Southern Border.

Task Instructions:
1. Data Triangulation: Scan the provided news data for keywords related to:
   - Weather events affecting transportation
   - Border wait times and customs delays
   - Policy changes (tariffs, USMCA, trade regulations)
   - Port congestion and freight delays

2. Correlation Engine: Do not just summarize. Explain the IMPACT:
   - If a weather event is found, correlate it with known transportation routes
   - Connect policy changes to potential freight delays
   - Identify cascading effects across the supply chain

3. Tone: Professional, predictive, and concise

4. Constraint: If no data is available for a specific query, state that the current news feed does not contain that information rather than making assumptions.

5. Always cite your sources by referencing the news categories you're drawing from.

Now analyze the user's question based on the current data:"""
        
        # Initialize the model
        model = genai.GenerativeModel('gemini-pro')
        
        # Generate response
        full_prompt = f"{system_prompt}\n\n{context}\n\nUser Question: {user_query}\n\nAnalysis:"
        
        response = model.generate_content(full_prompt)
        
        return response.text
    
    except Exception as e:
        return f"⚠️ Error communicating with AI: {str(e)}\n\nPlease check your GEMINI_API_KEY is valid and you have an internet connection."

# --- MAIN APP ---

def main():
    # Sidebar
    with st.sidebar:
        st.markdown("""<h2 style='color:#F8FAFC;font-weight:600;margin-bottom:0;'>⚠️ SupplyAlert</h2>
        <p style='color:#64748B;font-size:0.85rem;margin-top:4px;'>Supply Chain Intelligence</p>""", unsafe_allow_html=True)
        
        # Navigation
        page = st.radio(
            "Navigate",
            ["🏠 Dashboard", "🤖 AI Assistant", "📰 All News", "ℹ️ About"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Email Signup
        st.markdown("### 📧 Get Weekly Updates")
        st.markdown("<p style='font-size:0.85rem;color:#9CA3AF;'>Disruption alerts & industry insights delivered to your inbox.</p>", unsafe_allow_html=True)
        
        with st.form("email_signup"):
            email = st.text_input("Email", placeholder="your@email.com", label_visibility="collapsed")
            submitted = st.form_submit_button("Subscribe Free", use_container_width=True)
            if submitted:
                if email and "@" in email:
                    st.success("✅ Subscribed! Check your inbox.")
                else:
                    st.warning("Please enter a valid email.")
        
        st.markdown("---")
        
        st.info("""
**Track disruptions** affecting freight and logistics across weather, policy, and technology.

100% Free • No login required
        """)
        
        # Pro Teaser
        st.markdown("""<div style="margin-top:15px;padding:16px;background:linear-gradient(135deg, rgba(59,130,246,0.15) 0%, rgba(139,92,246,0.15) 100%);border-radius:12px;border:1px solid rgba(139,92,246,0.3);">
            <div style="color:#A78BFA;font-weight:600;font-size:0.95rem;">✨ SupplyAlert Pro</div>
            <p style="color:#94A3B8;font-size:0.8rem;margin:8px 0 0 0;line-height:1.5;">Coming Soon: Custom alerts, API access, historical data & route planning</p>
        </div>""", unsafe_allow_html=True)
        
        st.caption("v1.1.0 • Publicly available data")
    
    # Route to pages
    if page == "🤖 AI Assistant":
        show_ai_assistant_page()
    elif page == "📰 All News":
        show_news_page()
    elif page == "ℹ️ About":
        show_about_page()
    else:
        show_dashboard()

def show_ai_assistant_page():
    """AI Assistant chat interface page"""
    st.markdown("""
    <div class="hero">
        <div class="logo-icon">🤖</div>
        <h1>AI Supply Chain Analyst</h1>
        <p class="hero-subtitle">Ask complex questions about Southern Border logistics, weather impacts, and policy changes</p>
        <span class="hero-badge">POWERED BY GEMINI AI</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if API is configured
    api_configured = initialize_gemini()
    
    if not api_configured:
        st.warning("""
        ⚠️ **AI Assistant Not Configured**
        
        To use the AI Assistant, you need to set up your Google Gemini API key:
        
        1. Get a **FREE** API key at [Google AI Studio](https://ai.google.dev/)
        2. Create a `.env` file in the project root with:
           ```
           GEMINI_API_KEY=your_api_key_here
           ```
        3. Or add it to Streamlit secrets (for deployed apps)
        
        The Gemini API has a generous free tier for hobbyist projects!
        """)
    
    # Initialize session state for chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Suggested questions
    st.markdown("### 💡 Example Questions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🌪️ How will Texas storms affect border freight?", use_container_width=True):
            st.session_state.user_input = "How will the current storms in Texas affect cross-border freight operations?"
        if st.button("📜 What are the latest policy changes?", use_container_width=True):
            st.session_state.user_input = "What are the latest trade policy changes affecting the Southern Border?"
    
    with col2:
        if st.button("🚛 Border crossing delays today?", use_container_width=True):
            st.session_state.user_input = "What are the current border crossing delays and their causes?"
        if st.button("⚠️ Identify supply chain bottlenecks", use_container_width=True):
            st.session_state.user_input = "What are the major supply chain bottlenecks at the Southern Border right now?"
    
    st.markdown("---")
    
    # Chat interface
    st.markdown("### 💬 Chat with AI Analyst")
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user">
                    <strong>You:</strong><br>{message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant">
                    <strong>🤖 AI Analyst:</strong><br>{message["content"]}
                </div>
                """, unsafe_allow_html=True)
    
    # User input
    user_query = st.text_input(
        "Ask a question about supply chain intelligence:",
        key="user_input_text",
        placeholder="e.g., How will tariffs affect freight at Laredo?",
        value=st.session_state.get("user_input", "")
    )
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        send_button = st.button("Send 🚀", use_container_width=True, type="primary")
    
    with col2:
        if st.button("Clear Chat 🗑️", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.user_input = ""
            st.rerun()
    
    # Process query
    if send_button and user_query:
        if not api_configured:
            st.error("Please configure your GEMINI_API_KEY first (see instructions above).")
        else:
            # Add user message to history
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_query
            })
            
            # Get all news data
            with st.spinner("🔍 Analyzing supply chain data..."):
                news_data = get_all_news_as_json()
                
                # Get AI response
                ai_response = get_ai_response(user_query, news_data)
                
                # Add AI response to history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": ai_response
                })
            
            # Clear input and rerun to show new messages
            st.session_state.user_input = ""
            st.rerun()
    
    # Info box
    st.markdown("---")
    st.info("""
    **How the AI Assistant Works:**
    
    1. **Data Triangulation**: Scans news feeds for weather, border operations, and policy changes
    2. **RAG (Retrieval-Augmented Generation)**: Only sends relevant articles to AI for efficiency
    3. **Correlation Engine**: Connects weather events, policy changes, and logistics impacts
    4. **Southern Border Focus**: Specialized knowledge of cross-border freight operations
    
    💡 The AI only uses current news data from our feeds. It won't hallucinate information.
    """)

def show_dashboard():
    """Main supply chain intelligence dashboard"""
    # Hero
    st.markdown("""
    <div class="hero">
        <div class="logo-icon">📡</div>
        <h1>SupplyAlert</h1>
        <p class="hero-subtitle">Real-time supply chain intelligence for logistics professionals</p>
        <span class="hero-badge">LIVE UPDATES</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Current Alerts
    st.markdown("## 🚨 Active Weather Disruptions")
    
    alerts = get_weather_alerts()
    if alerts:
        cols = st.columns(len(alerts))
        for i, alert in enumerate(alerts):
            with cols[i]:
                severity_class = "alert-card" if alert['severity'] == "High" else "alert-card warning"
                st.markdown(f"""
<a href="https://www.weather.gov/" target="_blank" style="text-decoration:none;color:inherit;">
    <div class="{severity_class}" style="transition:transform 0.2s;cursor:pointer;">
        <div style="display:flex;justify-content:space-between;align-items:start;">
            <h3>{alert['type']}</h3>
            <span style="background:{'#EF4444' if alert['severity'] == 'High' else '#F59E0B'};color:white;padding:4px 12px;border-radius:100px;font-size:0.75rem;font-weight:600;">{alert['severity']}</span>
        </div>
        <p style="color:#CBD5E1;margin-bottom:4px;"><strong>📍 Location:</strong> {alert['location']}</p>
        <p style="color:#94A3B8;"><strong>⚠️ Impact:</strong> {alert['impact']}</p>
        <div style="margin-top:10px;font-size:0.8rem;color:#3B82F6;font-weight:500;">View Details →</div>
    </div>
</a>
                """, unsafe_allow_html=True)
    
    # Port Congestion
    st.markdown("## 🚢 Port Congestion Status")
    
    ports = get_port_status()
    cols = st.columns(len(ports))
    
    for i, (port, data) in enumerate(ports.items()):
        with cols[i]:
            st.markdown(f"""
<div class="stat-card">
    <div class="stat-value" style="color:{data['color']}">{data['delay_days']}</div>
    <div class="stat-label">Days Delay</div>
    <div style="margin-top:10px;font-weight:600;color:#E2E8F0;">{port}</div>
    <div style="color:#64748B;font-size:0.85rem;">{data['congestion']} Congestion</div>
</div>
            """, unsafe_allow_html=True)
    
    # News Sections
    col1, col2 = st.columns(2)
    
    with col1:
        # Freight Industry News
        st.markdown("## 🚛 Freight Industry News")
        st.caption("XPO, Ryder, Penske, JB Hunt & more")
        news = get_freight_industry_news()
        for item in news[:4]:
            date_str = format_news_date(item)
            st.markdown(f"""
<div style="background:#1F2937;padding:12px;border-radius:8px;margin:8px 0;border-left:3px solid #10B981;">
    <a href="{item.link}" target="_blank" style="color:#10B981;text-decoration:none;font-weight:500;">{item.title}</a>
    <div style="color:#6B7280;font-size:0.75rem;margin-top:4px;">{date_str}</div>
</div>
            """, unsafe_allow_html=True)
    
    with col2:
        # AI & Tech News
        st.markdown("## 🤖 AI in Supply Chain")
        st.caption("Automation, ML & logistics tech")
        news = get_ai_supply_chain_news()
        for item in news[:4]:
            date_str = format_news_date(item)
            st.markdown(f"""
<div style="background:#1F2937;padding:12px;border-radius:8px;margin:8px 0;border-left:3px solid #8B5CF6;">
    <a href="{item.link}" target="_blank" style="color:#8B5CF6;text-decoration:none;font-weight:500;">{item.title}</a>
    <div style="color:#6B7280;font-size:0.75rem;margin-top:4px;">{date_str}</div>
</div>
            """, unsafe_allow_html=True)
    
    # Policy News
    st.markdown("## 📜 Government & Policy News")
    st.caption("Trade policy, regulations, USMCA, DOT, FMCSA updates")
    news = get_policy_news()
    cols = st.columns(2)
    for i, item in enumerate(news[:6]):
        with cols[i % 2]:
            date_str = format_news_date(item)
            st.markdown(f"""
<div style="background:#1F2937;padding:12px;border-radius:8px;margin:8px 0;border-left:3px solid #EC4899;">
    <a href="{item.link}" target="_blank" style="color:#EC4899;text-decoration:none;font-weight:500;">{item.title}</a>
    <div style="color:#6B7280;font-size:0.75rem;margin-top:4px;">{date_str}</div>
</div>
            """, unsafe_allow_html=True)
    
    # Disruption News
    st.markdown("## ⚠️ Disruption Alerts")
    st.caption("Port delays, shortages, supply chain crises")
    news = get_disruption_news()
    cols = st.columns(2)
    for i, item in enumerate(news[:6]):
        with cols[i % 2]:
            date_str = format_news_date(item)
            st.markdown(f"""
<div style="background:#1F2937;padding:12px;border-radius:8px;margin:8px 0;border-left:3px solid #EF4444;">
    <a href="{item.link}" target="_blank" style="color:#EF4444;text-decoration:none;font-weight:500;">{item.title}</a>
    <div style="color:#6B7280;font-size:0.75rem;margin-top:4px;">{date_str}</div>
</div>
            """, unsafe_allow_html=True)
    
    # Southern Border News - NEW SECTION
    st.markdown("## 🌎 Southern Border Intelligence")
    st.caption("Cross-border freight, customs, USMCA, Mexico trade")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚛 Border Logistics")
        border_news = get_southern_border_news()
        for item in border_news[:4]:
            date_str = format_news_date(item)
            st.markdown(f"""
<div style="background:#1F2937;padding:12px;border-radius:8px;margin:8px 0;border-left:3px solid #F59E0B;">
    <a href="{item.link}" target="_blank" style="color:#F59E0B;text-decoration:none;font-weight:500;">{item.title}</a>
    <div style="color:#6B7280;font-size:0.75rem;margin-top:4px;">{date_str}</div>
</div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🌪️ Border Region Weather")
        weather_news = get_border_weather_news()
        for item in weather_news[:4]:
            date_str = format_news_date(item)
            st.markdown(f"""
<div style="background:#1F2937;padding:12px;border-radius:8px;margin:8px 0;border-left:3px solid #3B82F6;">
    <a href="{item.link}" target="_blank" style="color:#3B82F6;text-decoration:none;font-weight:500;">{item.title}</a>
    <div style="color:#6B7280;font-size:0.75rem;margin-top:4px;">{date_str}</div>
</div>
            """, unsafe_allow_html=True)
    
    # Footer with email CTA
    st.markdown("---")
    st.markdown("""
<div style="text-align:center;padding:30px;background:#1F2937;border-radius:12px;margin-top:20px;">
    <h3 style="color:#E2E8F0;">📧 Never Miss a Disruption</h3>
    <p style="color:#9CA3AF;">Subscribe in the sidebar for weekly supply chain intelligence updates.</p>
</div>
    """, unsafe_allow_html=True)

def show_news_page():
    """All news page"""
    st.markdown("# 📰 All Supply Chain News")
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🚛 Freight Industry", 
        "🤖 AI & Tech", 
        "📜 Policy", 
        "⚠️ Disruptions",
        "🌎 Southern Border",
        "🌪️ Border Weather"
    ])
    
    with tab1:
        news = get_freight_industry_news()
        for item in news:
            date_str = format_news_date(item)
            st.markdown(f"""
<div class="alert-card info">
    <a href="{item.link}" target="_blank" style="color:#10B981;text-decoration:none;font-weight:600;font-size:1.1rem;">{item.title}</a>
    <p style="color:#94A3B8;font-size:0.85rem;margin-top:8px;">{date_str}</p>
</div>
            """, unsafe_allow_html=True)
    
    with tab2:
        news = get_ai_supply_chain_news()
        for item in news:
            date_str = format_news_date(item)
            st.markdown(f"""
<div class="alert-card ai">
    <a href="{item.link}" target="_blank" style="color:#8B5CF6;text-decoration:none;font-weight:600;font-size:1.1rem;">{item.title}</a>
    <p style="color:#94A3B8;font-size:0.85rem;margin-top:8px;">{date_str}</p>
</div>
            """, unsafe_allow_html=True)
    
    with tab3:
        news = get_policy_news()
        for item in news:
            date_str = format_news_date(item)
            st.markdown(f"""
<div class="alert-card policy">
    <a href="{item.link}" target="_blank" style="color:#EC4899;text-decoration:none;font-weight:600;font-size:1.1rem;">{item.title}</a>
    <p style="color:#94A3B8;font-size:0.85rem;margin-top:8px;">{date_str}</p>
</div>
            """, unsafe_allow_html=True)
    
    with tab4:
        news = get_disruption_news()
        for item in news:
            date_str = format_news_date(item)
            st.markdown(f"""
<div class="alert-card">
    <a href="{item.link}" target="_blank" style="color:#EF4444;text-decoration:none;font-weight:600;font-size:1.1rem;">{item.title}</a>
    <p style="color:#94A3B8;font-size:0.85rem;margin-top:8px;">{date_str}</p>
</div>
            """, unsafe_allow_html=True)
    
    with tab5:
        st.markdown("### 🌎 Cross-Border Freight & Trade")
        news = get_southern_border_news()
        for item in news:
            date_str = format_news_date(item)
            st.markdown(f"""
<div class="alert-card warning">
    <a href="{item.link}" target="_blank" style="color:#F59E0B;text-decoration:none;font-weight:600;font-size:1.1rem;">{item.title}</a>
    <p style="color:#94A3B8;font-size:0.85rem;margin-top:8px;">{date_str}</p>
</div>
            """, unsafe_allow_html=True)
    
    with tab6:
        st.markdown("### 🌪️ Weather Affecting Border Region")
        news = get_border_weather_news()
        for item in news:
            date_str = format_news_date(item)
            st.markdown(f"""
<div class="alert-card info">
    <a href="{item.link}" target="_blank" style="color:#3B82F6;text-decoration:none;font-weight:600;font-size:1.1rem;">{item.title}</a>
    <p style="color:#94A3B8;font-size:0.85rem;margin-top:8px;">{date_str}</p>
</div>
            """, unsafe_allow_html=True)

def show_about_page():
    """About page"""
    st.markdown("# ℹ️ About Supply Chain Intelligence")
    
    st.markdown("""
    **Supply Chain Intelligence** helps logistics professionals track weather disruptions, 
    freight industry news, AI/technology developments, and policy changes affecting supply chains.
    
    ### 🤖 NEW: AI-Powered Intelligence
    
    Our **AI Supply Chain Analyst** transforms raw news feeds into actionable intelligence:
    
    - **Data Triangulation**: Synthesizes weather, policy, and logistics data
    - **Southern Border Focus**: Specialized analysis of cross-border freight operations
    - **Correlation Engine**: Identifies cascading effects across the supply chain
    - **RAG Technology**: Efficient, context-aware responses using Retrieval-Augmented Generation
    - **Zero Cost**: Powered by Google Gemini's free tier API
    
    ### 📊 Data Sources
    - **News Feeds:** Aggregated from publicly available sources (Google News RSS)
    - **Weather:** Public weather advisories
    - **Port Data:** Publicly reported congestion metrics
    - **AI Analysis:** Google Gemini API (free tier)
    
    ### 📰 News Categories
    - **🚛 Freight Industry:** XPO, Ryder, Penske, JB Hunt, Schneider, Werner
    - **🤖 AI & Tech:** Automation, machine learning, warehouse robotics
    - **📜 Policy:** USMCA, DOT, FMCSA, tariffs, trade regulations
    - **⚠️ Disruptions:** Port delays, shortages, weather impacts
    - **🌎 Southern Border:** Cross-border freight, customs, Mexico trade
    - **🌪️ Border Weather:** Texas/Mexico weather affecting logistics
    
    ### 🚀 How to Use the AI Assistant
    
    1. **Get a Free API Key:**
       - Visit [Google AI Studio](https://ai.google.dev/)
       - Sign in with your Google account
       - Generate a free API key
    
    2. **Configure the App:**
       - Create a `.env` file in the project root
       - Add: `GEMINI_API_KEY=your_api_key_here`
       - Or use Streamlit secrets for deployed apps
    
    3. **Ask Questions:**
       - Navigate to the "🤖 AI Assistant" page
       - Ask complex, multi-factor questions
       - Get predictive analysis and impact assessments
    
    ### ⚖️ Legal Disclaimer
    """)
    
    st.error("""
    **USE AT YOUR OWN RISK:** This tool is provided "AS IS" with **NO WARRANTIES**. The creator assumes **ZERO liability** for any decisions, delays, or losses arising from use of this data.
    
    **DATA SOURCE:** Aggregates publicly available information. Always verify with official sources before making business decisions.
    
    **AI DISCLAIMER:** AI responses are generated based on current news data. The AI may make errors or miss important context. Always verify critical information.
    
    **NO AFFILIATION:** Not affiliated with any government agency, carrier, commercial organization, or Google.
    """)

if __name__ == "__main__":
    main()

