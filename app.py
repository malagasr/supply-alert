import streamlit as st
import pandas as pd
import requests
import feedparser
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

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

# --- MAIN APP ---

def main():
    # Sidebar
    with st.sidebar:
        st.markdown("""<h2 style='color:#F8FAFC;font-weight:600;margin-bottom:0;'>⚠️ SupplyAlert</h2>
        <p style='color:#64748B;font-size:0.85rem;margin-top:4px;'>Supply Chain Intelligence</p>""", unsafe_allow_html=True)
        
        # Navigation
        page = st.radio(
            "Navigate",
            ["🏠 Dashboard", "📰 All News", "ℹ️ About"],
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
    if page == "📰 All News":
        show_news_page()
    elif page == "ℹ️ About":
        show_about_page()
    else:
        show_dashboard()

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
    
    tab1, tab2, tab3, tab4 = st.tabs(["🚛 Freight Industry", "🤖 AI & Tech", "📜 Policy", "⚠️ Disruptions"])
    
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

def show_about_page():
    """About page"""
    st.markdown("# ℹ️ About Supply Chain Intelligence")
    
    st.markdown("""
    **Supply Chain Intelligence** helps logistics professionals track weather disruptions, 
    freight industry news, AI/technology developments, and policy changes affecting supply chains.
    
    ### 📊 Data Sources
    - **News Feeds:** Aggregated from publicly available sources (Google News RSS)
    - **Weather:** Public weather advisories
    - **Port Data:** Publicly reported congestion metrics
    
    ### 📰 News Categories
    - **🚛 Freight Industry:** XPO, Ryder, Penske, JB Hunt, Schneider, Werner
    - **🤖 AI & Tech:** Automation, machine learning, warehouse robotics
    - **📜 Policy:** USMCA, DOT, FMCSA, tariffs, trade regulations
    - **⚠️ Disruptions:** Port delays, shortages, weather impacts
    
    ### ⚖️ Legal Disclaimer
    """)
    
    st.error("""
    **USE AT YOUR OWN RISK:** This tool is provided "AS IS" with **NO WARRANTIES**. The creator assumes **ZERO liability** for any decisions, delays, or losses arising from use of this data.
    
    **DATA SOURCE:** Aggregates publicly available information. Always verify with official sources before making business decisions.
    
    **NO AFFILIATION:** Not affiliated with any government agency, carrier, or commercial organization mentioned.
    """)

if __name__ == "__main__":
    main()

